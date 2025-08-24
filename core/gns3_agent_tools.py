#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GNS3 intelligent agent tools module.

Provides various tool functions required by intelligent agents,
supporting multi-language adaptation.
"""

import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from .get_topology_info import TopologyManager
from .get_config_info import DeviceConfigManager
from .get_all_devices_config import DeviceConfigCollector
from .get_interface_connections import InterfaceConnectionManager
from .language_adapter import get_message, format_device_info, format_project_info, format_skip_reason, language_adapter


class GNS3AgentTools:
    """GNS3 intelligent agent toolset."""
    
    def __init__(self, server_url: str, telnet_host: str):
        self.server_url = server_url
        self.telnet_host = telnet_host
        
        # Initialize managers
        self.topology_manager = TopologyManager(server_url)
        self.config_manager = DeviceConfigManager(telnet_host)
        self.collector = DeviceConfigCollector(server_url, telnet_host)
        self.interface_manager = InterfaceConnectionManager(server_url)
        
        # Cache related attributes
        self.projects_cache = {}
        self.devices_cache = {}
        self.last_cache_update = None
    
    def update_cache(self, force=False):
        """Update cache."""
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
        """Get topology information (including devices and interface connections)."""
        try:
            self.update_cache()
            topology_data = self.projects_cache.get('topology_data', {})
            
            if not topology_data:
                return get_message("no_topology_found")
            
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
                
                # Add interface connection information
                if links:
                    result += "\n   🔗 设备连接关系:\n"
                    # Build mapping from node ID to node name
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
            return get_message("get_topology_failed", str(e))
    
    def get_device_config(self, device_name: str) -> str:
        """Get device configuration."""
        try:
            self.update_cache()
            
            # Search for device
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
            return get_message("get_device_config_failed", device_name, str(e))
    
    def list_devices(self) -> str:
        """List all devices."""
        try:
            self.update_cache()
            
            result = get_message("configurable_devices_list") + "\n\n"
            total_devices = 0
            
            for project_name, project_devices in self.devices_cache.items():
                configurable_devices = project_devices.get('configurable_devices', [])
                
                if configurable_devices:
                    if language_adapter.current_config.use_english:
                        result += f"📁 Project: {project_name}\n"
                    else:
                        result += f"📁 项目: {project_name}\n"
                    
                    for device in configurable_devices:
                        name = device.get('name', 'Unknown')
                        device_type = device.get('node_type') or device.get('type', 'unknown')
                        status = device.get('status', 'unknown')
                        console = device.get('console', 'N/A')
                        
                        status_emoji = "🟢" if status == "started" else "🔴"
                        result += format_device_info(name, device_type, console) + "\n"
                        total_devices += 1
                    
                    result += "\n"
            
            if total_devices == 0:
                result += get_message("no_configurable_devices") + "\n"
            else:
                result += get_message("total_devices", total_devices) + "\n"
            
            return result
            
        except Exception as e:
            return get_message("get_device_list_failed", str(e))
    
    def get_project_status(self) -> str:
        """Get project status."""
        try:
            self.update_cache()
            
            opened_projects = self.projects_cache.get('opened_projects', [])
            
            if not opened_projects:
                return get_message("no_open_projects")
            
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
            return get_message("get_project_status_failed", str(e))
    
    def build_context(self) -> str:
        """Build system context."""
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
        """Extract device name from text."""
        # Common device name patterns
        patterns = [
            r'([Rr]-\d+)',  # R-1, R-2
            r'([Ss]witch-\d+)',  # Switch-1
            r'([Rr]outer-\d+)',  # Router-1
            r'([A-Za-z]+\d+)',  # Generic pattern
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_interface_name(self, label_info) -> str:
        """Extract interface name from label information."""
        if isinstance(label_info, dict):
            return label_info.get('text', 'Unknown')
        elif isinstance(label_info, str):
            return label_info
        else:
            return 'Unknown'
    
    def get_interface_connections(self, device_name: str = None) -> str:
        """Get device interface connection information."""
        return self.interface_manager.get_device_interfaces(device_name)
    
    def get_network_connections_summary(self) -> str:
        """Get network connections summary."""
        return self.interface_manager.get_network_connections_summary()
