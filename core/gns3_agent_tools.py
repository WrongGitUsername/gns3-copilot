#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GNS3 智能代理工具模块
提供智能代理所需的各种工具函数，支持多语言适配
"""

import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from .get_topology_info import TopologyManager
from .get_config_info import DeviceConfigManager
from .get_all_devices_config import DeviceConfigCollector
from .get_interface_connections import InterfaceConnectionManager
from .language_adapter import get_message, format_device_info, format_project_info, format_skip_reason


class GNS3AgentTools:
    """GNS3智能代理工具集"""
    
    def __init__(self, server_url: str, telnet_host: str):
        self.server_url = server_url
        self.telnet_host = telnet_host
        
        # 初始化管理器
        self.topology_manager = TopologyManager(server_url)
        self.config_manager = DeviceConfigManager(telnet_host)
        self.collector = DeviceConfigCollector(server_url, telnet_host)
        self.interface_manager = InterfaceConnectionManager(server_url)
        
        # 缓存相关
        self.projects_cache = {}
        self.devices_cache = {}
        self.last_cache_update = None
    
    def update_cache(self, force=False):
        """更新缓存"""
        now = datetime.now()
        
        if (not force and self.last_cache_update and 
            (now - self.last_cache_update).seconds < 300):
            return
        
        try:
            print(get_message("updating_project_info"))
            opened_projects = self.topology_manager.get_opened_projects()
            topology_data = self.topology_manager.get_all_topology_info()
            
            self.projects_cache = {
                'opened_projects': opened_projects,
                'topology_data': topology_data
            }
            
            self.devices_cache = {}
            for project_name, project_info in topology_data.items():
                devices = project_info.get('nodes', [])
                configurable_devices = self.collector.filter_configurable_devices(devices)
                self.devices_cache[project_name] = {
                    'all_devices': devices,
                    'configurable_devices': configurable_devices
                }
            
            self.last_cache_update = now
            print(get_message("cache_updated", len(opened_projects)))
            
        except Exception as e:
            print(get_message("error_occurred", str(e)))
    
    def get_topology_info(self) -> str:
        """获取拓扑信息（包含设备和接口连接）"""
        try:
            self.update_cache()
            topology_data = self.projects_cache.get('topology_data', {})
            
            if not topology_data:
                return "❌ 没有找到拓扑信息"
            
            result = "🗺️ 网络拓扑信息：\n\n"
            
            for project_name, project_info in topology_data.items():
                nodes = project_info.get('nodes', [])
                links = project_info.get('links', [])
                
                result += f"📋 项目: {project_name}\n"
                result += f"   📱 设备总数: {len(nodes)}\n"
                result += f"   🔗 链路总数: {len(links)}\n"
                
                if nodes:
                    result += "   📱 设备列表:\n"
                    for node in nodes:
                        name = node.get('name', 'Unknown')
                        node_type = node.get('node_type') or node.get('type', 'unknown')
                        status = node.get('status', 'unknown')
                        status_emoji = "🟢" if status == "started" else "🔴"
                        result += f"      {status_emoji} {name} ({node_type})\n"
                
                # 添加接口连接信息
                if links:
                    result += "\n   🔗 设备连接关系:\n"
                    # 构建节点ID到名称的映射
                    node_name_map = {node.get('node_id'): node.get('name', 'Unknown') for node in nodes}
                    
                    for i, link in enumerate(links, 1):
                        link_nodes = link.get('nodes', [])
                        if len(link_nodes) == 2:
                            node1, node2 = link_nodes
                            
                            node1_name = node_name_map.get(node1.get('node_id'), 'Unknown')
                            node1_interface = self._extract_interface_name(node1.get('label'))
                            
                            node2_name = node_name_map.get(node2.get('node_id'), 'Unknown')
                            node2_interface = self._extract_interface_name(node2.get('label'))
                            
                            result += f"      {i:2d}. {node1_name} {node1_interface} ↔ {node2_name} {node2_interface}\n"
                        else:
                            result += f"      {i:2d}. 复杂链路 (节点数: {len(link_nodes)})\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"❌ 获取拓扑信息失败: {e}"
    
    def get_device_config(self, device_name: str) -> str:
        """获取设备配置"""
        try:
            self.update_cache()
            
            # 查找设备
            device_info = None
            device_name_lower = device_name.lower()
            
            for project_name, project_devices in self.devices_cache.items():
                for device in project_devices['configurable_devices']:
                    if device['name'].lower() == device_name_lower:
                        device_info = {'device': device, 'project': project_name}
                        break
                if device_info:
                    break
            
            if not device_info:
                return f"❌ 找不到设备 '{device_name}'。请先查看设备列表。"
            
            device = device_info['device']
            console_port = device.get('console')
            
            print(f"🔌 正在连接 {device_name} (端口: {console_port})...")
            
            config = self.config_manager.get_device_config(device_name, console_port)
            
            if not config:
                return f"❌ 无法获取 {device_name} 的配置"
            
            lines = config.split('\n')
            summary = f"""✅ 成功获取 {device_name} 配置

📊 配置统计：
   - 总行数: {len(lines)}
   - 总字符数: {len(config)}
   - 配置大小: {len(config.encode('utf-8')) / 1024:.1f} KB

📄 配置内容（前20行）：
{chr(10).join(lines[:20])}
...

如需完整配置分析，请说："详细分析{device_name}配置\""""
            
            return summary
            
        except Exception as e:
            return f"❌ 获取 {device_name} 配置失败: {e}"
    
    def list_devices(self) -> str:
        """列出所有设备"""
        try:
            self.update_cache()
            
            result = "📱 可配置设备列表：\n\n"
            total_devices = 0
            
            for project_name, project_devices in self.devices_cache.items():
                configurable_devices = project_devices.get('configurable_devices', [])
                
                if configurable_devices:
                    result += f"📁 项目: {project_name}\n"
                    
                    for device in configurable_devices:
                        name = device.get('name', 'Unknown')
                        device_type = device.get('node_type') or device.get('type', 'unknown')
                        status = device.get('status', 'unknown')
                        console = device.get('console', 'N/A')
                        
                        status_emoji = "🟢" if status == "started" else "🔴"
                        result += f"   {status_emoji} {name} ({device_type}) - 端口:{console}\n"
                        total_devices += 1
                    
                    result += "\n"
            
            if total_devices == 0:
                result += "❌ 没有找到可配置的设备\n"
            else:
                result += f"📊 总计: {total_devices} 个可配置设备\n"
            
            return result
            
        except Exception as e:
            return f"❌ 获取设备列表失败: {e}"
    
    def get_project_status(self) -> str:
        """获取项目状态"""
        try:
            self.update_cache()
            
            opened_projects = self.projects_cache.get('opened_projects', [])
            
            if not opened_projects:
                return "❌ 没有找到打开的项目"
            
            result = f"📋 项目状态信息 ({len(opened_projects)} 个打开的项目)：\n\n"
            
            for project in opened_projects:
                project_name = project[0]
                project_id = project[1]
                
                project_devices = self.devices_cache.get(project_name, {})
                all_devices = project_devices.get('all_devices', [])
                configurable_devices = project_devices.get('configurable_devices', [])
                
                result += f"📁 项目: {project_name}\n"
                result += f"   🆔 ID: {project_id}\n"
                result += f"   📱 总设备: {len(all_devices)}\n"
                result += f"   ⚙️ 可配置设备: {len(configurable_devices)}\n"
                
                started_count = len([d for d in all_devices if d.get('status') == 'started'])
                result += f"   🟢 运行中: {started_count}\n"
                result += f"   🔴 已停止: {len(all_devices) - started_count}\n\n"
            
            return result
            
        except Exception as e:
            return f"❌ 获取项目状态失败: {e}"
    
    def build_context(self) -> str:
        """构建系统上下文"""
        self.update_cache()
        
        opened_projects = self.projects_cache.get('opened_projects', [])
        device_count = sum(len(p.get('configurable_devices', [])) for p in self.devices_cache.values())
        
        context = f"""
GNS3服务器: {self.server_url}
打开的项目数: {len(opened_projects)}
可配置设备数: {device_count}
最后缓存更新: {self.last_cache_update.strftime('%H:%M:%S') if self.last_cache_update else '未更新'}
"""
        
        return context
    
    def extract_device_name(self, text: str) -> Optional[str]:
        """从文本中提取设备名称"""
        # 常见的设备名称模式
        patterns = [
            r'([Rr]-\d+)',  # R-1, R-2
            r'([Ss]witch-\d+)',  # Switch-1
            r'([Rr]outer-\d+)',  # Router-1
            r'([A-Za-z]+\d+)',  # 通用模式
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_interface_name(self, label_info) -> str:
        """从标签信息中提取接口名称"""
        if isinstance(label_info, dict):
            return label_info.get('text', 'Unknown')
        elif isinstance(label_info, str):
            return label_info
        else:
            return 'Unknown'
    
    def get_interface_connections(self, device_name: str = None) -> str:
        """获取设备接口连接信息"""
        return self.interface_manager.get_device_interfaces(device_name)
    
    def get_network_connections_summary(self) -> str:
        """获取网络连接汇总"""
        return self.interface_manager.get_network_connections_summary()
