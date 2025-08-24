#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG增强的智能命令执行器
结合向量化知识库和现有命令库
"""

import os
import sys
import re
from typing import List, Dict, Optional
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.network_rag_kb import NetworkTroubleshootingRAG
from core.network_commands_kb import get_command_suggestions, search_commands_by_keyword
from core.language_adapter import get_prompt_template, get_message, language_adapter

class RAGEnhancedCommandExecutor:
    """RAG增强的命令执行器"""
    
    def __init__(self, telnet_host: str, llm, use_rag: bool = True):
        """
        初始化RAG增强的命令执行器
        
        Args:
            telnet_host: Telnet主机地址
            llm: LLM模型实例  
            use_rag: 是否使用RAG知识库
        """
        # 导入原有的智能命令执行器
        from core.intelligent_command_executor import IntelligentCommandExecutor
        
        # 继承原有功能
        self.base_executor = IntelligentCommandExecutor(telnet_host, llm)
        
        # RAG知识库
        self.use_rag = use_rag
        self.rag_kb = None
        
        # 设备IP缓存
        self.device_ip_cache = {}
        
        if use_rag:
            try:
                self.rag_kb = NetworkTroubleshootingRAG()
                if hasattr(language_adapter, 'current_config'):
                    print(get_message("rag_kb_initialized"))
                else:
                    print("✅ RAG knowledge base initialized successfully")
            except Exception as e:
                print(f"⚠️ RAG knowledge base initialization failed, will use basic knowledge base: {e}")
                self.use_rag = False
    
    def _is_valid_command(self, command: str) -> bool:
        """验证命令是否有效"""
        if not command or not command.strip():
            return False
            
        command = command.strip()
        
        # 检查命令是否以有效前缀开始
        valid_prefixes = ['show ', 'display ', 'ping ', 'traceroute ', 'debug ']
        if not any(command.startswith(prefix) for prefix in valid_prefixes):
            return False
        
        # 检查是否包含无效字符
        # 允许：字母、数字、空格、连字符、点号、斜杠、下划线
        invalid_chars_pattern = r'[^a-zA-Z0-9\s\-\./_]'
        if re.search(invalid_chars_pattern, command):
            return False
        
        # 检查是否包含通配符或占位符
        invalid_patterns = [
            r'\*+',           # 星号通配符
            r'\?+',           # 问号通配符  
            r'\.\.\.+',       # 省略号
            r'x\.x\.x\.x',    # IP占位符
            r'\*\*\*',        # 星号占位符
            r'___+',          # 下划线占位符
            r'show\s+\w+\s*\.\.\.', # 不完整命令（如show ip ro...）
        ]
        
        for pattern in invalid_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return False
        
        # 检查命令是否完整（不以...结尾）
        if command.endswith('...') or command.endswith('..'):
            return False
            
        return True
    
    def _get_relevant_commands_enhanced(self, query: str) -> List[Dict]:
        """增强的命令获取 - 结合RAG和基础知识库"""
        all_commands = []
        
        # 1. 基础知识库查询
        base_commands = get_command_suggestions(query, max_results=5)
        for cmd in base_commands:
            cmd['source'] = 'base_kb'
            all_commands.append(cmd)
        
        # 2. RAG知识库查询
        if self.use_rag and self.rag_kb:
            try:
                rag_results = self.rag_kb.search_commands(query, k=3)
                
                for result in rag_results:
                    # 从RAG结果中提取命令
                    for command in result['commands']:
                        cmd_info = {
                            'command': command,
                            'description': f"来自知识库: {result['summary'][:100]}...",
                            'purpose': "基于网络排错文档的建议",
                            'category': 'rag_suggested',
                            'score': result['score'],
                            'source': 'rag_kb',
                            'context': result['content'][:500]
                        }
                        all_commands.append(cmd_info)
                        
                print(get_message("rag_knowledge_base_returned").format(len([r for r in rag_results if r['commands']])))
                
            except Exception as e:
                print(f"⚠️ RAG查询失败: {e}")
        
        # 3. 关键词补充查询
        keywords = query.lower().split()
        for keyword in keywords[:3]:  # 限制关键词数量
            additional = search_commands_by_keyword(keyword)
            for cmd in additional:
                if not any(c["command"] == cmd["command"] for c in all_commands):
                    cmd['source'] = 'keyword_search'
                    all_commands.append(cmd)
        
        # 排序并去重
        unique_commands = {}
        for cmd in all_commands:
            command_key = cmd['command']
            if command_key not in unique_commands:
                unique_commands[command_key] = cmd
            else:
                # 保留评分更高的
                if cmd.get('score', 0) > unique_commands[command_key].get('score', 0):
                    unique_commands[command_key] = cmd
        
        # 按评分排序
        sorted_commands = sorted(
            unique_commands.values(), 
            key=lambda x: x.get('score', 0), 
            reverse=True
        )
        
        return sorted_commands[:8]  # 限制返回数量
    
    def _llm_command_selection_enhanced(self, query: str, commands: List[Dict]) -> List[str]:
        """增强的LLM命令选择 - 考虑RAG上下文"""
        
        # 构建命令文本，包含来源信息
        commands_text = []
        for cmd in commands:
            source_info = f"[{cmd.get('source', 'unknown')}]"
            cmd_line = f"- {cmd['command']}: {cmd['description']} {source_info}"
            
            # 如果是RAG命令，添加上下文
            if cmd.get('source') == 'rag_kb' and cmd.get('context'):
                cmd_line += f"\n  上下文: {cmd['context'][:200]}..."
                
            commands_text.append(cmd_line)
        
        commands_str = "\n".join(commands_text)
        
        # 判断查询复杂度
        query_lower = query.lower()
        complex_keywords = [
            '路由', 'route', '宣告', 'advertise', '数据库', 'database', 
            '配置', 'config', '详细', 'detail', '分析', 'analysis',
            '汇总', 'summary', '所有', 'all', '完整', 'complete',
            '故障', 'troubleshoot', '问题', 'problem', '排错', 'debug'
        ]
        
        simple_keywords = ['邻居', 'neighbor', '状态', 'status', '简单', 'brief']
        
        has_complex = any(keyword in query_lower for keyword in complex_keywords)
        has_simple = any(keyword in query_lower for keyword in simple_keywords)
        
        max_commands = 3 if has_complex else (2 if has_simple and has_complex else 1)
        
        # 更新语言配置
        language_adapter.update_language_config(query)
        
        # 增强的提示词
        prompt = get_prompt_template("rag_command_prompt", 
                                   query=query, 
                                   commands_str=commands_str, 
                                   max_commands=max_commands)

        try:
            response = self.base_executor.llm.invoke(prompt)
            content = response.content if hasattr(response, 'content') else str(response)
            
            # 解析命令
            selected = []
            for line in content.strip().split('\n'):
                line = line.strip()
                if line and not line.startswith('有效示例') and not line.startswith('无效示例') and not line.startswith('Valid Examples') and not line.startswith('Invalid Examples'):
                    # 清理可能的前缀
                    if line.startswith('- '):
                        line = line[2:].strip()
                    if line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
                        line = line[2:].strip()
                    
                    # 使用命令验证函数
                    if self._is_valid_command(line):
                        selected.append(line)
                        if len(selected) >= max_commands:
                            break
            
            if not selected and commands:
                # 如果没有选中任何命令，从候选列表中选择第一个有效的
                for cmd in commands:
                    if self._is_valid_command(cmd['command']):
                        selected = [cmd['command']]
                        break
            
            return selected[:max_commands]
            
        except Exception as e:
            print(f"⚠️ 增强LLM命令选择失败: {e}")
            return [cmd['command'] for cmd in commands[:max_commands]]
    
    def execute_intelligent_query(self, user_query: str, devices_info: List[Dict], 
                                target_device: str = None) -> str:
        """执行智能查询 - RAG增强版本"""
        try:
            # 检查是否为连通性查询，如果是则使用智能连通性分析
            if self._is_connectivity_query(user_query):
                return self._handle_connectivity_query(user_query, devices_info, target_device)
            
            print(get_message("using_rag_enhanced_command_selection"))
            
            # 1. 使用增强的命令获取
            relevant_commands = self._get_relevant_commands_enhanced(user_query)
            
            if not relevant_commands:
                return get_message("no_relevant_commands_found").format(user_query)
            
            print(get_message("found_relevant_commands_combined").format(len(relevant_commands)))
            
            # 2. 使用增强的LLM命令选择
            selected_commands = self._llm_command_selection_enhanced(user_query, relevant_commands)
            
            if not selected_commands:
                return get_message("llm_no_suitable_commands")
            
            print(get_message("llm_selected_commands", selected_commands))
            
            # 3. 使用基础执行器的其他功能
            # 确定目标设备
            target_devices = self.base_executor._determine_target_devices(
                user_query, devices_info, target_device
            )
            
            if not target_devices:
                return get_message("unable_to_determine_target_device")
            
            # 4. 执行命令并收集结果
            execution_results = []
            for device in target_devices:
                device_results = self.base_executor._execute_commands_on_device(
                    device, selected_commands
                )
                execution_results.append({
                    "device": device,
                    "results": device_results
                })
            
            # 5. 生成增强分析报告
            final_report = self._generate_enhanced_analysis(
                user_query, execution_results, selected_commands, relevant_commands
            )
            
            return final_report
            
        except Exception as e:
            return get_message("rag_enhanced_query_failed", e)
    
    def _generate_enhanced_analysis(self, query: str, execution_results: List[Dict], 
                                  commands: List[str], all_commands: List[Dict]) -> str:
        """生成增强分析报告"""
        
        # 基础报告
        base_report = self.base_executor._llm_result_analysis(
            query, execution_results, commands
        )
        
        # 添加RAG知识库建议
        rag_suggestions = []
        for cmd_info in all_commands:
            if cmd_info.get('source') == 'rag_kb':
                rag_suggestions.append({
                    'command': cmd_info['command'],
                    'context': cmd_info.get('context', ''),
                    'score': cmd_info.get('score', 0)
                })
        
        if rag_suggestions:
            rag_section = get_message("rag_knowledge_suggestions")
            for i, suggestion in enumerate(rag_suggestions[:3], 1):
                rag_section += f"{i}. {suggestion['command']}\n"
                rag_section += get_message("relevance_score").format(suggestion['score']) + "\n"
                if suggestion['context']:
                    rag_section += get_message("background_context").format(suggestion['context'][:150]) + "\n"
            
            base_report += rag_section
        
        return base_report
    
    def _is_connectivity_query(self, query: str) -> bool:
        """检查是否为连通性查询"""
        connectivity_keywords = ['ping', 'connectivity', 'connect', 'reachable', '连通', '连接', '通信', 'test connection']
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in connectivity_keywords)
    
    def _handle_connectivity_query(self, user_query: str, devices_info: List[Dict], 
                                 target_device: str = None) -> str:
        """处理连通性查询"""
        try:
            print(get_message("connectivity_query_detected"))
            
            # 解析查询以确定源设备和目标设备
            devices = [device['name'] for device in devices_info]
            source_device, target_device_name = self._parse_connectivity_query(user_query, devices, target_device)
            
            if not source_device or not target_device_name:
                return get_message("unable_to_determine_devices")
            
            # 获取目标设备的IP地址
            target_ip = self._get_device_ip(target_device_name, devices_info)
            if not target_ip:
                return get_message("unable_to_get_device_ip", target_device_name)
            
            # 构造并执行ping命令
            ping_command = f"ping {target_ip}"
            print(get_message("executing_ping_command", source_device, ping_command))
            
            # 使用基础执行器的命令执行方法
            result = self._execute_simple_command(source_device, ping_command, devices_info)
            
            return self._format_connectivity_result(source_device, target_device_name, target_ip, result)
            
        except Exception as e:
            return get_message("connectivity_test_failed", str(e))
    
    def _parse_connectivity_query(self, query: str, devices: List[str], target_device: str = None) -> tuple:
        """解析连通性查询，提取源设备和目标设备"""
        query_lower = query.lower()
        
        # 如果指定了目标设备，使用它作为源设备
        source_device = target_device
        target_device_name = None
        
        # 尝试从查询中提取设备名
        for device in devices:
            if device.lower() in query_lower:
                if not source_device:
                    source_device = device
                elif device != source_device:
                    target_device_name = device
                    break
        
        # 如果只找到一个设备，尝试提取IP地址模式
        if source_device and not target_device_name:
            import re
            ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
            ips = re.findall(ip_pattern, query)
            if ips:
                # 使用找到的IP作为目标
                return source_device, ips[0]
        
        return source_device, target_device_name
    
    def _get_device_ip(self, device_name: str, devices_info: List[Dict]) -> str:
        """获取设备的IP地址"""
        # 检查缓存
        if device_name in self.device_ip_cache:
            return self.device_ip_cache[device_name]
        
        try:
            # 执行show ip interface brief命令获取IP地址
            show_ip_result = self._execute_simple_command(device_name, "show ip interface brief", devices_info)
            
            # 解析结果提取IP地址
            ip_address = self._extract_ip_from_show_result(show_ip_result)
            
            if ip_address:
                # 缓存结果
                self.device_ip_cache[device_name] = ip_address
                return ip_address
            
        except Exception as e:
            print(get_message("getting_device_ip_failed", device_name, str(e)))
        
        return None
    
    def _extract_ip_from_show_result(self, show_result: str) -> str:
        """从show ip interface brief结果中提取IP地址"""
        import re
        
        # 查找有效的IP地址（排除127.0.0.1和0.0.0.0）
        ip_pattern = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
        ips = re.findall(ip_pattern, show_result)
        
        for ip in ips:
            if ip not in ['127.0.0.1', '0.0.0.0'] and not ip.startswith('0.'):
                return ip
        
        return None
    
    def _format_connectivity_result(self, source_device: str, target_device: str, 
                                  target_ip: str, ping_result: str) -> str:
        """格式化连通性测试结果"""
        result = get_message("connectivity_test_results")
        result += get_message("source_device", source_device) + "\n"
        result += get_message("target_device", target_device) + "\n"
        result += get_message("target_ip", target_ip) + "\n"
        result += get_message("test_command", f"ping {target_ip}") + "\n"
        result += get_message("execution_results")
        result += ping_result
        result += f"\n{'='*30}\n"
        
        return result
        
    def _execute_simple_command(self, device_name: str, command: str, devices_info: List[Dict]) -> str:
        """执行简单命令的封装方法"""
        try:
            # 查找设备的控制台端口
            device_info = None
            for device in devices_info:
                if device['name'] == device_name:
                    device_info = device
                    break
            
            if not device_info:
                if language_adapter.current_config.use_english:
                    return f"Device {device_name} not found"
                else:
                    return f"找不到设备 {device_name}"
            
            # 使用基础执行器的单命令执行方法
            result = self.base_executor._execute_single_command(
                device_name, 
                device_info['console'], 
                command
            )
            
            return result.get('output', '') if isinstance(result, dict) else str(result)
            
        except Exception as e:
            if language_adapter.current_config.use_english:
                return f"Command execution failed: {str(e)}"
            else:
                return f"执行命令失败: {str(e)}"

if __name__ == "__main__":
    # 测试RAG增强执行器
    from core.llm_manager import LLMManager
    
    llm_manager = LLMManager()
    
    # 创建RAG增强执行器
    rag_executor = RAGEnhancedCommandExecutor(
        telnet_host="192.168.102.1",
        llm=llm_manager.current_model,
        use_rag=True
    )
    
    # 测试命令获取
    test_query = "OSPF邻居无法建立连接"
    commands = rag_executor._get_relevant_commands_enhanced(test_query)
    
    print(f"\n🔍 查询: {test_query}")
    print(f"📋 找到 {len(commands)} 个相关命令:")
    
    for i, cmd in enumerate(commands, 1):
        print(f"{i}. {cmd['command']} [{cmd.get('source', 'unknown')}]")
        print(f"   {cmd['description']}")
