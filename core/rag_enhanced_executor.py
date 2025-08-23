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
            
            print(f"🤖 LLM选择的命令: {selected_commands}")
            
            # 3. 使用基础执行器的其他功能
            # 确定目标设备
            target_devices = self.base_executor._determine_target_devices(
                user_query, devices_info, target_device
            )
            
            if not target_devices:
                return f"❌ 无法确定目标设备"
            
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
            return f"❌ RAG增强查询执行失败: {e}"
    
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
            rag_section = "\n\n📚 RAG知识库补充建议:\n"
            for i, suggestion in enumerate(rag_suggestions[:3], 1):
                rag_section += f"{i}. {suggestion['command']}\n"
                rag_section += f"   相关度: {suggestion['score']:.2f}\n"
                if suggestion['context']:
                    rag_section += f"   背景: {suggestion['context'][:150]}...\n"
            
            base_report += rag_section
        
        return base_report

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
