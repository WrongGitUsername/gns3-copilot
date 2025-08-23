#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GNS3拓扑信息获取模块
提供获取GNS3项目拓扑信息和链路摘要的功能
"""

import os
from gns3fy import Gns3Connector, Project
from dotenv import load_dotenv
from .language_adapter import get_message, language_adapter

# 加载环境变量
load_dotenv()

class TopologyManager:
    """拓扑信息管理器"""
    
    def __init__(self, server_url=None):
        """
        初始化拓扑管理器
        
        Args:
            server_url: GNS3服务器URL，如果不指定则从环境变量获取
        """
        self.server_url = server_url or os.getenv("GNS3_SERVER_URL", "http://192.168.101.1:3080")
        self.server = Gns3Connector(url=self.server_url)
    
    def get_opened_projects(self):
        """获取所有打开的项目"""
        try:
            print(get_message("getting_project_summary"))
            projects_data = self.server.projects_summary(is_print=False)
            opened_projects = [project for project in projects_data if project[4] == "opened"]
            
            if not opened_projects:
                print(get_message("no_open_projects_found"))
                return []
            
            print(get_message("found_open_projects").format(len(opened_projects)))
            for project in opened_projects:
                print(get_message("project_name_id").format(project[0], project[1]))
            
            return opened_projects
            
        except Exception as e:
            print(get_message("get_project_summary_error").format(e))
            return []
    
    def get_all_topology_info(self):
        """获取所有打开项目的拓扑信息"""
        opened_projects = self.get_opened_projects()
        topology_data = {}
        
        for project in opened_projects:
            project_name = project[0]
            project_id = project[1]
            
            try:
                # 创建Project对象并获取详细信息
                from gns3fy import Project
                proj = Project(name=project_name, project_id=project_id, connector=self.server)
                proj.get()
                
                project_info = {
                    'nodes': [],
                    'links': []
                }
                
                # 获取节点信息
                if hasattr(proj, 'nodes') and proj.nodes:
                    for node in proj.nodes:
                        node_info = {
                            'name': node.name,
                            'node_type': node.node_type,
                            'status': node.status,
                            'console': getattr(node, 'console', None),
                            'node_id': node.node_id
                        }
                        project_info['nodes'].append(node_info)
                
                # 获取链路信息
                if hasattr(proj, 'links') and proj.links:
                    for link in proj.links:
                        link_info = {
                            'link_id': link.link_id,
                            'link_type': getattr(link, 'link_type', 'unknown'),
                            'nodes': []
                        }
                        
                        if hasattr(link, 'nodes') and link.nodes:
                            for link_node in link.nodes:
                                node_info = {
                                    'node_id': link_node.get('node_id', ''),
                                    'adapter_number': link_node.get('adapter_number', 0),
                                    'port_number': link_node.get('port_number', 0),
                                    'label': link_node.get('label', '')
                                }
                                link_info['nodes'].append(node_info)
                        
                        project_info['links'].append(link_info)
                
                topology_data[project_name] = project_info
                
            except Exception as e:
                print(f"获取项目 {project_name} 拓扑信息时发生错误: {e}")
                topology_data[project_name] = {'nodes': [], 'links': []}
        
        return topology_data

def main():
    """主函数，用于测试"""
    topology_manager = TopologyManager()
    
    # 获取打开的项目
    opened_projects = topology_manager.get_opened_projects()
    
    # 获取拓扑信息
    topology_data = topology_manager.get_all_topology_info()
    
    if opened_projects:
        print(f"\n成功获取 {len(opened_projects)} 个项目的拓扑信息")
        
        # 显示详细信息
        for project_name, project_info in topology_data.items():
            nodes_count = len(project_info.get('nodes', []))
            links_count = len(project_info.get('links', []))
            print(f"  - {project_name}: {nodes_count} 个节点, {links_count} 个链路")
    else:
        print("未找到任何项目")

if __name__ == "__main__":
    main()
