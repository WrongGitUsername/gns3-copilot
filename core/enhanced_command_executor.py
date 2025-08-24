#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced intelligent command executor.

Adds device configuration analysis and intelligent command construction functionality.
"""

import re
import time
import telnetlib
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from .intelligent_command_executor import IntelligentCommandExecutor
from .language_adapter import get_message, language_adapter

class EnhancedIntelligentCommandExecutor(IntelligentCommandExecutor):
    """Enhanced intelligent command executor."""
    
    def __init__(self, telnet_host: str, llm):
        super().__init__(telnet_host, llm)
        self.device_ip_cache = {}  # Cache device IP address information
    
    def execute_intelligent_query(self, user_query: str, devices_info: List[Dict], 
                                target_device: str = None) -> str:
        """
        Enhanced intelligent query execution.
        """
        try:
            # Check if it's a query requiring device-to-device communication
            if self._is_connectivity_query(user_query):
                return self._handle_connectivity_query(user_query, devices_info, target_device)
            
            # For other queries, use original logic
            return super().execute_intelligent_query(user_query, devices_info, target_device)
            
        except Exception as e:
            return f"❌ Enhanced intelligent query execution failed: {e}"
    
    def _is_connectivity_query(self, query: str) -> bool:
        """Determine if it's a connectivity query."""
        connectivity_keywords = [
            'ping', 'connectivity', 'reachability', 'test connection',
            'from', 'to', 'between', '连通性', '测试', 'reach'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in connectivity_keywords)
    
    def _handle_connectivity_query(self, user_query: str, devices_info: List[Dict], 
                                 target_device: str = None) -> str:
        """Handle connectivity query."""
        try:
            # 1. Parse device information from the query
            source_device, target_device_name = self._parse_connectivity_query(user_query, devices_info)
            
            if not source_device or not target_device_name:
                return self._fallback_to_basic_ping(user_query, devices_info, target_device)
            
            # 2. Get IP addresses of source and target devices
            source_ips = self._get_device_ip_addresses(source_device)
            target_ips = self._get_device_ip_addresses_by_name(target_device_name, devices_info)
            
            if not source_ips or not target_ips:
                return f"""⚠️  无法获取设备IP地址信息
                
📋 分析结果：
- 源设备: {source_device.get('name', 'Unknown')} 
- 目标设备: {target_device_name}
- 源设备IP: {'已获取' if source_ips else '未获取'}
- 目标设备IP: {'已获取' if target_ips else '未获取'}

💡 建议：
1. 请确保设备已正确配置IP地址
2. 检查设备是否在线
3. 或直接指定要测试的IP地址"""
            
            # 3. Construct intelligent ping commands
            ping_commands = self._construct_intelligent_ping_commands(source_ips, target_ips)
            
            # 4. Execute commands
            execution_results = []
            device_results = self._execute_commands_on_device(source_device, ping_commands)
            execution_results.append({
                "device": source_device,
                "results": device_results
            })
            
            # 5. Generate intelligent analysis report
            return self._generate_connectivity_report(
                user_query, source_device, target_device_name, 
                source_ips, target_ips, execution_results
            )
            
        except Exception as e:
            return f"❌ Connectivity query processing failed: {e}"
    
    def _parse_connectivity_query(self, query: str, devices_info: List[Dict]) -> Tuple[Dict, str]:
        """Parse device information from connectivity query."""
        device_names = [device['name'] for device in devices_info]
        
        # 查找查询中提到的设备
        found_devices = []
        for device_name in device_names:
            if device_name.lower() in query.lower():
                found_devices.append(device_name)
        
        if len(found_devices) >= 2:
            # 找到源和目标设备
            source_name = found_devices[0]
            target_name = found_devices[1]
            
            # 检查查询中的方向指示词
            if any(word in query.lower() for word in ['from', 'source']):
                # 如果有明确的方向指示，可能需要调整顺序
                pass
            
            source_device = next((d for d in devices_info if d['name'] == source_name), None)
            return source_device, target_name
        
        elif len(found_devices) == 1:
            # 只找到一个设备，尝试从查询中推断另一个
            device_name = found_devices[0]
            device = next((d for d in devices_info if d['name'] == device_name), None)
            
            # 尝试从查询中提取另一个设备名
            remaining_query = query.lower().replace(device_name.lower(), '')
            for other_device in device_names:
                if other_device.lower() in remaining_query:
                    return device, other_device
            
            return device, None
        
        return None, None
    
    def _get_device_ip_addresses(self, device: Dict) -> List[str]:
        """获取设备的IP地址"""
        device_name = device['name']
        console_port = device.get('console')
        
        if not console_port:
            return []
        
        # 检查缓存
        cache_key = f"{device_name}:ip_addresses"
        if cache_key in self.device_ip_cache:
            return self.device_ip_cache[cache_key]
        
        # 执行命令获取IP地址
        ip_commands = [
            "show ip interface brief",
            "show interfaces | include Internet"
        ]
        
        ip_addresses = []
        for command in ip_commands:
            try:
                result = self._execute_single_command(device_name, console_port, command)
                if result['success']:
                    ips = self._extract_ip_addresses(result['output'])
                    ip_addresses.extend(ips)
                    if ip_addresses:  # 如果第一个命令成功，就不需要第二个
                        break
            except:
                continue
        
        # 过滤掉无效IP
        valid_ips = [ip for ip in ip_addresses if self._is_valid_ip(ip) and not ip.startswith('127.')]
        
        # 缓存结果
        self.device_ip_cache[cache_key] = valid_ips
        
        return valid_ips
    
    def _get_device_ip_addresses_by_name(self, device_name: str, devices_info: List[Dict]) -> List[str]:
        """根据设备名获取IP地址"""
        device = next((d for d in devices_info if d['name'] == device_name), None)
        if device:
            return self._get_device_ip_addresses(device)
        return []
    
    def _extract_ip_addresses(self, command_output: str) -> List[str]:
        """从命令输出中提取IP地址"""
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        ips = re.findall(ip_pattern, command_output)
        
        # 过滤掉明显不是接口IP的地址
        valid_ips = []
        for ip in ips:
            # 跳过特殊地址
            if ip in ['0.0.0.0', '255.255.255.255']:
                continue
            
            # 跳过广播地址（末尾为255的地址）
            if ip.endswith('.255'):
                continue
            
            # 接受所有其他IP地址（包括公网IP和私网IP）
            # 因为在实验环境中可能使用各种IP地址
            valid_ips.append(ip)
        
        return list(set(valid_ips))  # 去重
    
    def _is_valid_ip(self, ip: str) -> bool:
        """验证IP地址格式"""
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        
        try:
            for part in parts:
                num = int(part)
                if num < 0 or num > 255:
                    return False
            return True
        except ValueError:
            return False
    
    def _construct_intelligent_ping_commands(self, source_ips: List[str], target_ips: List[str]) -> List[str]:
        """构造智能ping命令"""
        commands = []
        
        # 选择最佳的源IP和目标IP组合
        for target_ip in target_ips[:2]:  # 最多测试2个目标IP
            if source_ips:
                # 如果有多个源IP，选择第一个作为源地址
                source_ip = source_ips[0]
                commands.append(f"ping {target_ip} source {source_ip}")
            else:
                # 如果没有获取到源IP，使用默认ping
                commands.append(f"ping {target_ip}")
        
        # 如果没有获取到目标IP，但有源IP，可以尝试ping网关
        if not target_ips and source_ips:
            for source_ip in source_ips[:1]:
                # 尝试ping同网段的网关
                ip_parts = source_ip.split('.')
                gateway_ip = '.'.join(ip_parts[:-1] + ['1'])
                commands.append(f"ping {gateway_ip} source {source_ip}")
        
        return commands if commands else ["ping 8.8.8.8"]  # fallback
    
    def _generate_connectivity_report(self, query: str, source_device: Dict, target_device_name: str,
                                    source_ips: List[str], target_ips: List[str], 
                                    execution_results: List[Dict]) -> str:
        """生成连通性分析报告"""
        
        report = f"""🔍 Network Connectivity Analysis Report
{'='*60}

📋 Query Information:
   - User Request: {query}
   - Source Device: {source_device['name']}
   - Target Device: {target_device_name}
   - Test Type: ICMP Ping Test

📊 Device IP Configuration:
   - Source IPs: {', '.join(source_ips) if source_ips else 'Not detected'}
   - Target IPs: {', '.join(target_ips) if target_ips else 'Not detected'}

"""
        
        # 分析执行结果
        for device_result in execution_results:
            device_name = device_result["device"]["name"]
            report += f"🔍 Test Results from {device_name}:\n"
            
            for cmd_result in device_result["results"]:
                command = cmd_result["command"]
                success = cmd_result["success"]
                output = cmd_result["output"]
                
                if success:
                    # 分析ping结果
                    ping_analysis = self._analyze_ping_output(output)
                    report += f"   ✅ Command: {command}\n"
                    report += f"   📊 Result: {ping_analysis}\n\n"
                else:
                    report += f"   ❌ Command: {command} - Failed\n"
                    report += f"   📝 Output: {output[:200]}...\n\n"
        
        # 添加建议
        report += self._get_connectivity_recommendations(source_ips, target_ips, execution_results)
        
        return report
    
    def _analyze_ping_output(self, output: str) -> str:
        """分析ping命令输出"""
        if "Success rate is" in output:
            # 提取成功率
            success_match = re.search(r'Success rate is (\d+) percent', output)
            if success_match:
                success_rate = success_match.group(1)
                if success_rate == "100":
                    return f"✅ Connectivity confirmed - {success_rate}% success rate"
                elif int(success_rate) > 0:
                    return f"⚠️  Partial connectivity - {success_rate}% success rate"
                else:
                    return f"❌ No connectivity - {success_rate}% success rate"
        
        if "Destination unreachable" in output:
            return "❌ Destination unreachable"
        
        if "Request timeout" in output:
            return "⏰ Request timeout - possible connectivity issue"
        
        return "📝 Ping executed - check detailed output"
    
    def _get_connectivity_recommendations(self, source_ips: List[str], target_ips: List[str], 
                                        execution_results: List[Dict]) -> str:
        """生成连通性建议"""
        recommendations = "💡 Recommendations:\n"
        
        if not source_ips:
            recommendations += "   - Configure IP addresses on source device interfaces\n"
        
        if not target_ips:
            recommendations += "   - Verify target device IP configuration\n"
            recommendations += "   - Ensure target device is reachable\n"
        
        recommendations += "   - Check routing tables: show ip route\n"
        recommendations += "   - Verify interface status: show ip interface brief\n"
        recommendations += "   - Check for ACLs that might block ICMP traffic\n"
        
        return recommendations
    
    def _fallback_to_basic_ping(self, user_query: str, devices_info: List[Dict], 
                              target_device: str = None) -> str:
        """回退到基本ping功能"""
        return super().execute_intelligent_query(user_query, devices_info, target_device)
