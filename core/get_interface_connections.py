#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GNS3 device interface connection information retrieval module.

Provides functionality to retrieve device interface status and interconnection relationships.
"""

import os
from typing import Dict, List, Optional, Tuple
from .language_adapter import get_message, language_adapter

try:
    from .get_topology_info import TopologyManager
except ImportError:
    # Import for standalone testing
    from get_topology_info import TopologyManager

class InterfaceConnectionManager:
    """Interface connection information manager."""
    
    def __init__(self, server_url=None):
        """
        Initialize interface connection manager.
        
        Args:
            server_url: GNS3 server URL, if not specified, get from environment variables
        """
        self.server_url = server_url or os.getenv("GNS3_SERVER_URL", "http://192.168.101.1:3080")
        self.topology_manager = TopologyManager(server_url)
        self._node_name_cache = {}  # Cache for node ID to name mapping
    
    def _build_node_cache(self, topology_data: Dict) -> None:
        """Build node ID to name mapping cache."""
        self._node_name_cache.clear()
        
        for project_name, project_info in topology_data.items():
            nodes = project_info.get('nodes', [])
            for node in nodes:
                node_id = node.get('node_id')
                node_name = node.get('name')
                if node_id and node_name:
                    self._node_name_cache[node_id] = node_name
    
    def _extract_interface_name(self, label_info) -> str:
        """Extract interface name from label information."""
        if isinstance(label_info, dict):
            return label_info.get('text', 'Unknown')
        elif isinstance(label_info, str):
            return label_info
        else:
            return 'Unknown'
    
    def get_device_interfaces(self, device_name: str = None) -> str:
        """
        获取设备接口信息和连接状态
        
        Args:
            device_name: 设备名称，如果为None则显示所有设备的接口
            
        Returns:
            格式化的接口信息字符串
        """
        try:
            topology_data = self.topology_manager.get_all_topology_info()
            if not topology_data:
                return "❌ 无法获取拓扑数据"
            
            self._build_node_cache(topology_data)
            
            result = "🔌 设备接口连接信息：\n\n"
            
            for project_name, project_info in topology_data.items():
                nodes = project_info.get('nodes', [])
                links = project_info.get('links', [])
                
                # 如果指定了设备名称，只显示该设备
                if device_name:
                    target_nodes = [node for node in nodes if node.get('name', '').lower() == device_name.lower()]
                    if not target_nodes:
                        continue
                    nodes = target_nodes
                
                result += f"📋 项目: {project_name}\n"
                
                # 构建接口连接映射
                interface_connections = self._build_interface_connections(links)
                
                for node in nodes:
                    node_name = node.get('name', 'Unknown')
                    node_type = node.get('node_type', 'unknown')
                    status = node.get('status', 'unknown')
                    status_emoji = "🟢" if status == "started" else "🔴"
                    node_id = node.get('node_id')
                    
                    result += f"\n🖥️ {status_emoji} 设备: {node_name} ({node_type})\n"
                    
                    # 获取该设备的所有接口
                    device_interfaces = self._get_device_interfaces_from_links(node_id, links)
                    
                    if device_interfaces:
                        result += "   📡 接口状态:\n"
                        for interface in device_interfaces:
                            interface_name = interface['name']
                            adapter = interface['adapter']
                            port = interface['port']
                            connection_info = interface_connections.get(f"{node_id}:{adapter}:{port}", {})
                            
                            if connection_info:
                                remote_device = connection_info['remote_device']
                                remote_interface = connection_info['remote_interface']
                                result += f"      🔗 {interface_name} (A{adapter}/P{port}) ↔ {remote_device} {remote_interface}\n"
                            else:
                                result += f"      ⚫ {interface_name} (A{adapter}/P{port}) - 未连接\n"
                    else:
                        result += "   📡 未发现可用接口\n"
                
                result += "\n"
            
            return result if result.strip() != "🔌 设备接口连接信息：" else f"❌ 未找到设备 '{device_name}' 的接口信息"
            
        except Exception as e:
            return f"❌ 获取接口信息失败: {e}"
    
    def _build_interface_connections(self, links: List[Dict]) -> Dict[str, Dict]:
        """构建接口连接映射"""
        connections = {}
        
        for link in links:
            link_nodes = link.get('nodes', [])
            if len(link_nodes) == 2:
                node1, node2 = link_nodes
                
                # 第一个节点到第二个节点的连接
                node1_key = f"{node1.get('node_id')}:{node1.get('adapter_number')}:{node1.get('port_number')}"
                node1_interface = self._extract_interface_name(node1.get('label'))
                node2_name = self._node_name_cache.get(node2.get('node_id'), 'Unknown')
                node2_interface = self._extract_interface_name(node2.get('label'))
                
                connections[node1_key] = {
                    'remote_device': node2_name,
                    'remote_interface': node2_interface
                }
                
                # 第二个节点到第一个节点的连接
                node2_key = f"{node2.get('node_id')}:{node2.get('adapter_number')}:{node2.get('port_number')}"
                node1_name = self._node_name_cache.get(node1.get('node_id'), 'Unknown')
                
                connections[node2_key] = {
                    'remote_device': node1_name,
                    'remote_interface': node1_interface
                }
        
        return connections
    
    def _get_device_interfaces_from_links(self, node_id: str, links: List[Dict]) -> List[Dict]:
        """从链路信息中提取设备的所有接口"""
        interfaces = []
        seen_interfaces = set()
        
        for link in links:
            link_nodes = link.get('nodes', [])
            for link_node in link_nodes:
                if link_node.get('node_id') == node_id:
                    adapter = link_node.get('adapter_number', 0)
                    port = link_node.get('port_number', 0)
                    interface_key = f"{adapter}:{port}"
                    
                    if interface_key not in seen_interfaces:
                        interface_name = self._extract_interface_name(link_node.get('label'))
                        interfaces.append({
                            'name': interface_name,
                            'adapter': adapter,
                            'port': port
                        })
                        seen_interfaces.add(interface_key)
        
        # 按适配器和端口排序
        interfaces.sort(key=lambda x: (x['adapter'], x['port']))
        return interfaces
    
    def get_network_connections_summary(self) -> str:
        """获取网络连接汇总信息"""
        try:
            topology_data = self.topology_manager.get_all_topology_info()
            if not topology_data:
                return "❌ 无法获取拓扑数据"
            
            self._build_node_cache(topology_data)
            
            result = "🌐 网络连接汇总：\n\n"
            
            for project_name, project_info in topology_data.items():
                links = project_info.get('links', [])
                
                result += f"📋 项目: {project_name}\n"
                result += f"   🔗 总链路数: {len(links)}\n\n"
                
                if links:
                    result += "   📡 连接详情:\n"
                    for i, link in enumerate(links, 1):
                        link_nodes = link.get('nodes', [])
                        if len(link_nodes) == 2:
                            node1, node2 = link_nodes
                            
                            node1_name = self._node_name_cache.get(node1.get('node_id'), 'Unknown')
                            node1_interface = self._extract_interface_name(node1.get('label'))
                            
                            node2_name = self._node_name_cache.get(node2.get('node_id'), 'Unknown')
                            node2_interface = self._extract_interface_name(node2.get('label'))
                            
                            result += f"      {i:2d}. {node1_name} {node1_interface} ↔ {node2_name} {node2_interface}\n"
                        else:
                            result += f"      {i:2d}. 复杂链路 (节点数: {len(link_nodes)})\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"❌ 获取连接汇总失败: {e}"

def main():
    """主函数，用于测试"""
    manager = InterfaceConnectionManager()
    
    print("=== 所有设备接口信息 ===")
    print(manager.get_device_interfaces())
    
    print("\n=== 网络连接汇总 ===")
    print(manager.get_network_connections_summary())
    
    print("\n=== R-1 设备接口 ===")
    print(manager.get_device_interfaces("R-1"))

if __name__ == "__main__":
    main()
