#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能命令执行器
基于RAG和LLM的动态网络命令执行系统
"""

import time
import telnetlib
import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from .network_commands_kb import get_command_suggestions, search_commands_by_keyword
from .language_adapter import get_message, language_adapter


class IntelligentCommandExecutor:
    """智能命令执行器"""
    
    def __init__(self, telnet_host: str, llm):
        """
        初始化智能命令执行器
        
        Args:
            telnet_host: Telnet主机地址
            llm: LLM模型实例
        """
        self.telnet_host = telnet_host
        self.llm = llm
        self.command_cache = {}  # 缓存执行结果
    
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
    
    def execute_intelligent_query(self, user_query: str, devices_info: List[Dict], 
                                target_device: str = None) -> str:
        """
        智能执行用户查询
        
        Args:
            user_query: 用户查询字符串
            devices_info: 设备信息列表
            target_device: 目标设备名称（可选）
        
        Returns:
            格式化的查询结果
        """
        try:
            # 1. 使用RAG获取相关命令
            relevant_commands = self._get_relevant_commands(user_query)
            
            if not relevant_commands:
                return get_message("no_relevant_commands_found").format(user_query)
            
            # 2. 让LLM分析并选择最佳命令
            selected_commands = self._llm_command_selection(user_query, relevant_commands)
            
            if not selected_commands:
                return get_message("llm_no_suitable_commands")
            
            print(get_message("llm_selected_commands").format(selected_commands))
            
            # 3. 确定目标设备
            target_devices = self._determine_target_devices(user_query, devices_info, target_device)
            
            # 4. 执行命令并收集结果
            execution_results = []
            for device in target_devices:
                device_results = self._execute_commands_on_device(
                    device, selected_commands
                )
                execution_results.append({
                    "device": device,
                    "results": device_results
                })
            
            # 5. 让LLM分析结果并生成报告
            final_report = self._llm_result_analysis(
                user_query, execution_results, selected_commands
            )
            
            return final_report
            
        except Exception as e:
            return f"❌ 智能查询执行失败: {e}"
    
    def _get_relevant_commands(self, query: str) -> List[Dict]:
        """使用RAG获取相关命令"""
        # 获取命令建议
        suggestions = get_command_suggestions(query, max_results=10)
        
        # 如果建议不足，尝试关键词搜索
        if len(suggestions) < 3:
            keywords = query.lower().split()
            for keyword in keywords:
                additional = search_commands_by_keyword(keyword)
                for cmd in additional:
                    if not any(s["command"] == cmd["command"] for s in suggestions):
                        suggestions.append({
                            "command": cmd["command"],
                            "description": cmd["description"],
                            "purpose": cmd["purpose"],
                            "category": cmd["category"],
                            "score": 1
                        })
        
        return suggestions[:8]  # 限制返回数量以避免token溢出
    
    def _llm_command_selection(self, query: str, commands: List[Dict]) -> List[str]:
        """让LLM选择最适合的命令"""
        commands_text = "\n".join([
            f"- {cmd['command']}: {cmd['description']} (用途: {cmd['purpose']})"
            for cmd in commands
        ])
        
        # 判断查询的复杂度，决定返回命令数量
        query_lower = query.lower()
        
        # 复杂查询关键词（这些查询通常需要多个命令）
        complex_keywords = [
            '路由', 'route', '宣告', 'advertise', '数据库', 'database', 
            '配置', 'config', '详细', 'detail', '分析', 'analysis',
            '汇总', 'summary', '所有', 'all', '完整', 'complete'
        ]
        
        # 简单查询关键词（这些查询通常只需要一个命令）
        simple_keywords = [
            '邻居', 'neighbor', '状态', 'status', '简单', 'brief'
        ]
        
        # 检查是否包含复杂查询关键词
        has_complex = any(keyword in query_lower for keyword in complex_keywords)
        has_simple = any(keyword in query_lower for keyword in simple_keywords)
        
        # 决定命令数量：如果有复杂关键词，允许更多命令
        if has_complex and not (has_simple and not has_complex):
            max_commands = 2
        else:
            max_commands = 1
        
        prompt = f"""
作为网络工程师，请分析用户查询并选择最适合的命令。

用户查询: {query}

可用命令列表:
{commands_text}

重要约束：
- 只返回有效的网络命令
- 不要使用通配符（* ? ...）
- 不要使用占位符（x.x.x.x, ***_, ..., 等）
- 不要使用不完整的命令（show ip ro...）
- 命令只能包含字母、数字、空格、连字符、点号和斜杠
- 每个命令必须完整且可执行

请选择最适合回答用户查询的{"1个最重要的命令" if max_commands == 1 else "1-2个命令，按重要性排序"}。
只返回命令本身，每行一个，不要其他文字。

{"对于简单状态查询，通常只需要一个主要命令即可。" if max_commands == 1 else "对于复杂查询，可能需要多个命令来获得完整信息。"}

有效示例：
show ip ospf neighbor
show ip route ospf
show running-config

无效示例（请勿使用）：
show ip route x.x.x.x
show ip ro...
show * interface
ping ***
"""
        
        try:
            response = self.llm.invoke(prompt)
            content = response.content if hasattr(response, 'content') else str(response)
            
            # 解析LLM选择的命令
            selected = []
            for line in content.strip().split('\n'):
                line = line.strip()
                if line and not line.startswith('例如') and not line.startswith('有效示例') and not line.startswith('无效示例') and not line.startswith('show:') and not line.startswith('#'):
                    # 清理可能的前缀
                    if line.startswith('- '):
                        line = line[2:].strip()
                    if line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
                        line = line[2:].strip()
                    if ':' in line and not line.startswith('show'):
                        line = line.split(':')[0].strip()
                    
                    # 验证命令是否有效
                    if self._is_valid_command(line):
                        selected.append(line)
                        if len(selected) >= max_commands:
                            break
                        
                        # 对于简单查询，只要找到一个命令就停止
                        if max_commands == 1 and len(selected) >= 1:
                            break
            
            # 如果没有解析到命令，使用第一个推荐命令
            if not selected and commands:
                selected = [commands[0]['command']]
            
            return selected[:max_commands]  # 限制命令数量
            
            return selected[:3]  # 最多3个命令
            
        except Exception as e:
            print(get_message("llm_command_selection_failed").format(e))
            # 默认选择前2个高分命令
            return [cmd['command'] for cmd in commands[:2]]
    
    def _determine_target_devices(self, query: str, devices_info: List[Dict], 
                                target_device: str = None) -> List[Dict]:
        """确定目标设备"""
        if target_device:
            # 查找指定设备
            for device in devices_info:
                if device['name'].lower() == target_device.lower():
                    return [device]
            return []
        
        # 从查询中提取所有设备名称
        query_lower = query.lower()
        matched_devices = []
        
        # 检查查询中是否包含多个设备名称
        for device in devices_info:
            device_name = device['name'].lower()
            if device_name in query_lower:
                matched_devices.append(device)
        
        # 如果找到了多个设备，返回所有匹配的设备
        if matched_devices:
            return matched_devices
        
        # 如果没有指定设备，返回所有可配置设备（最多5个避免执行时间过长）
        return devices_info[:5]
    
    def _execute_commands_on_device(self, device: Dict, commands: List[str]) -> List[Dict]:
        """在设备上执行命令列表"""
        results = []
        device_name = device['name']
        console_port = device.get('console')
        
        if not console_port:
            return [{
                "command": "connection_check",
                "output": f"设备 {device_name} 没有可用的控制台端口",
                "success": False
            }]
        
        print(get_message("executing_commands_on_device").format(len(commands), device_name))
        
        for command in commands:
            result = self._execute_single_command(device_name, console_port, command)
            results.append(result)
            time.sleep(1)  # 避免命令执行过快
        
        return results
    
    def _execute_single_command(self, device_name: str, console_port: int, 
                              command: str) -> Dict:
        """执行单个命令"""
        try:
            print(get_message("executing_command").format(command))
            
            # 检查缓存
            cache_key = f"{device_name}:{console_port}:{command}"
            if cache_key in self.command_cache:
                cache_time, cached_result = self.command_cache[cache_key]
                # 如果缓存时间小于5分钟，使用缓存
                if time.time() - cache_time < 300:
                    print(get_message("using_cached_result"))
                    return cached_result
            
            # 连接到设备
            tn = telnetlib.Telnet(self.telnet_host, console_port, timeout=15)
            
            # 发送回车，确保到达命令提示符
            tn.write(b"\r\n")
            time.sleep(2)
            
            # 清空缓冲区
            tn.read_very_eager()
            
            # 发送命令
            tn.write(f"{command}\r\n".encode('ascii'))
            
            # 等待命令开始执行
            time.sleep(3)
            
            # 收集完整输出
            full_output = ""
            max_iterations = 20  # 增加最大迭代次数
            no_output_count = 0
            
            for i in range(max_iterations):
                output = tn.read_very_eager().decode('ascii', errors='ignore')
                
                if output:
                    full_output += output
                    no_output_count = 0
                    
                    # 检查是否有分页提示
                    if "--More--" in output or "-- More --" in output or "(more)" in output.lower():
                        tn.write(b" ")  # 发送空格继续显示
                        time.sleep(1)
                        continue
                    
                    # 检查是否返回到命令提示符
                    if (output.endswith("#") or output.endswith("> ") or 
                        output.endswith("# ") or output.endswith(">")):
                        print(get_message("command_prompt_detected"))
                        break
                        
                else:
                    no_output_count += 1
                    # 如果连续3次没有输出，可能命令已完成
                    if no_output_count >= 3:
                        print(get_message("no_output_timeout"))
                        break
                
                time.sleep(0.5)  # 减少等待时间，增加检查频率
            
            # 最后再读取一次，确保没有遗漏
            time.sleep(1)
            final_output = tn.read_very_eager().decode('ascii', errors='ignore')
            if final_output:
                full_output += final_output
            
            # 关闭连接
            tn.close()
            
            # 清理输出
            cleaned_output = self._clean_command_output(full_output, command)
            
            result = {
                "command": command,
                "output": cleaned_output,
                "success": True,
                "timestamp": datetime.now().isoformat(),
                "raw_output_length": len(full_output)
            }
            
            # 缓存结果
            self.command_cache[cache_key] = (time.time(), result)
            
            print(get_message("command_execution_complete").format(len(cleaned_output)))
            return result
            
        except Exception as e:
            error_result = {
                "command": command,
                "output": f"命令执行失败: {e}",
                "success": False,
                "timestamp": datetime.now().isoformat()
            }
            print(get_message("command_execution_failed").format(e))
            return error_result
    
    def _clean_command_output(self, raw_output: str, command: str) -> str:
        """清理命令输出"""
        if not raw_output:
            return ""
        
        lines = raw_output.split('\n')
        clean_lines = []
        command_found = False
        
        for line in lines:
            # 去除回车符
            line = line.replace('\r', '').strip()
            
            # 跳过空行
            if not line:
                continue
            
            # 找到命令行本身，从下一行开始收集输出
            if not command_found and command in line:
                command_found = True
                continue
            
            # 如果还没找到命令行，跳过
            if not command_found:
                continue
            
            # 过滤掉各种提示符和控制字符
            if (line.endswith('#') and len(line) < 10) or \
               (line.endswith('>') and len(line) < 10) or \
               line.endswith('# ') or \
               line.endswith('> ') or \
               "--More--" in line or \
               "-- More --" in line or \
               "(more)" in line.lower() or \
               line.startswith('%') or \
               line.startswith('show ') or \
               line == command:
                continue
            
            # 如果检测到新的命令提示符（表示命令结束），停止收集
            if (line.endswith('#') or line.endswith('>')) and len(line) > 10:
                # 检查是否是路径提示符（包含设备名的完整提示符）
                continue
            
            clean_lines.append(line)
        
        result = '\n'.join(clean_lines)
        
        # 额外清理：移除开头和结尾的提示符行
        lines = result.split('\n')
        while lines and (not lines[0] or lines[0].endswith(('#', '>'))):
            lines.pop(0)
        while lines and (not lines[-1] or lines[-1].endswith(('#', '>'))):
            lines.pop()
        
        return '\n'.join(lines)
    
    def _llm_result_analysis(self, query: str, execution_results: List[Dict], 
                           commands: List[str]) -> str:
        """让LLM分析执行结果并生成报告"""
        
        # 构建结果摘要
        results_summary = []
        for device_result in execution_results:
            device_name = device_result["device"]["name"]
            results_summary.append(f"\\n设备: {device_name}")
            
            for cmd_result in device_result["results"]:
                command = cmd_result["command"]
                success = cmd_result["success"]
                output = cmd_result["output"]
                
                if success and output.strip():
                    # 截断过长的输出
                    if len(output) > 1000:
                        output = output[:1000] + "\\n... (输出已截断)"
                    results_summary.append(f"  命令: {command}")
                    results_summary.append(f"  输出: {output}")
                else:
                    results_summary.append(f"  命令: {command} - 执行失败或无输出")
        
        results_text = "\\n".join(results_summary)
        
        analysis_prompt = f"""
作为专业的网络工程师，请分析以下网络命令执行结果，并提供专业的分析报告。

用户查询: {query}
执行的命令: {', '.join(commands)}

命令执行结果:
{results_text}

请提供一份结构化的分析报告，包括：
1. 执行摘要
2. 关键发现
3. 状态分析
4. 问题识别（如果有）
5. 建议和下一步操作

请使用中文回复，保持专业性和简洁性。
"""
        
        try:
            analysis = self.llm.invoke(analysis_prompt)
            content = analysis.content if hasattr(analysis, 'content') else str(analysis)
            
            # 构建最终报告
            report = f"""🔍 智能网络查询分析报告
{'='*50}

📋 查询信息:
   - 用户查询: {query}
   - 执行命令: {', '.join(commands)}
   - 查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
   - 涉及设备: {len(execution_results)} 台

🤖 AI 分析结果:
{content}

📊 详细执行结果:
{results_text}
"""
            return report
            
        except Exception as e:
            # LLM分析失败时返回基础报告
            return f"""🔍 网络查询执行报告
{'='*50}

📋 查询信息:
   - 用户查询: {query}
   - 执行命令: {', '.join(commands)}
   - 查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
   - 涉及设备: {len(execution_results)} 台

❌ AI分析失败: {e}

📊 执行结果:
{results_text}
"""
