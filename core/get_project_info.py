#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GNS3 project information retrieval module.

Provides functionality to retrieve detailed information about GNS3 projects.
"""

import os
from gns3fy import Gns3Connector, Project
from dotenv import load_dotenv
from .language_adapter import get_message, language_adapter

# Load environment variables
load_dotenv()

class ProjectInfoManager:
    """Project information manager."""
    
    def __init__(self, server_url=None):
        """
        Initialize project information manager.
        
        Args:
            server_url: GNS3 server address, if not specified, get from environment variables
        """
        self.server_url = server_url or os.getenv("GNS3_SERVER_URL", "http://192.168.101.1:3080")
        self.server = Gns3Connector(self.server_url)
    
    def get_projects_summary(self):
        """
        Get project summary.
        
        Returns:
            list: Project summary list
        """
        try:
            return self.server.projects_summary(is_print=False)
        except Exception as e:
            print(get_message("get_project_summary_error").format(e))
            return []
    
    def get_opened_projects(self):
        """
        Get all opened projects.
        
        Returns:
            list: List of opened project information
        """
        projects_summary = self.get_projects_summary()
        # Filter projects currently in "opened" status (4th element of tuple is Status)
        opened_projects = [p for p in projects_summary if p[4] == "opened"]
        return opened_projects
    
    def get_project_details(self, project_name, project_id):
        """
        获取指定项目的详细信息
        
        Args:
            project_name: 项目名称
            project_id: 项目ID
            
        Returns:
            dict: 项目详细信息
        """
        try:
            # 创建Project对象
            project = Project(name=project_name, project_id=project_id, connector=self.server)
            
            # 获取项目详细信息
            project.get()
            
            project_details = {
                'name': project_name,
                'id': project_id,
                'nodes': [],
                'links': []
            }
            
            # 获取节点信息
            if project.nodes:
                for node in project.nodes:
                    node_info = {
                        'name': node.name,
                        'type': node.node_type,
                        'status': node.status,
                        'console': node.console,
                        'id': node.node_id
                    }
                    project_details['nodes'].append(node_info)
            
            # 获取链路信息
            if project.links:
                for link in project.links:
                    link_info = {
                        'id': link.link_id,
                        'type': link.link_type,
                        'nodes': []
                    }
                    
                    for link_node in link.nodes:
                        link_node_info = {
                            'label': link_node.get('label', link_node.get('node_label', '')),
                            'adapter': link_node.get('adapter_number', 0),
                            'port': link_node.get('port_number', 0)
                        }
                        link_info['nodes'].append(link_node_info)
                    
                    project_details['links'].append(link_info)
            
            return project_details
            
        except Exception as e:
            print(get_message("get_project_details_error").format(project_name, e))
            return {'name': project_name, 'id': project_id, 'nodes': [], 'links': []}
    
    def get_all_opened_projects_info(self):
        """
        获取所有打开项目的详细信息
        
        Returns:
            dict: 项目名称到项目详细信息的映射
        """
        opened_projects = self.get_opened_projects()
        projects_info = {}
        
        if not opened_projects:
            print(get_message("no_open_projects"))
            return projects_info
        
        print(get_message("current_open_projects"))
        for p in opened_projects:
            print(get_message("project_name_id").format(p[0], p[1]))
    
    def get_all_opened_projects_info(self):
        """
        获取所有打开项目的详细信息
        
        Returns:
            dict: 项目名称到项目详细信息的映射
        """
        opened_projects = self.get_opened_projects()
        projects_info = {}
        
        if not opened_projects:
            print(get_message("no_open_projects"))
            return projects_info
        
        print(get_message("current_open_projects"))
        for p in opened_projects:
            print(get_message("project_name_id").format(p[0], p[1]))
        
        # 遍历每个打开的项目
        for proj_info in opened_projects:
            project_name = proj_info[0]
            project_id = proj_info[1]
            
            print(get_message("project_topology_info").format(project_name))
            project_details = self.get_project_details(project_name, project_id)
            projects_info[project_name] = project_details
            
            # 输出节点信息
            print(get_message("node_list"))
            if project_details['nodes']:
                for node in project_details['nodes']:
                    print(get_message("node_details").format(node['name'], node['type'], node['status'], node['console']))
            else:
                print(get_message("no_nodes"))
            
            # 输出链路信息
            print(get_message("link_list"))
            if project_details['links']:
                for link in project_details['links']:
                    print(get_message("link_details").format(link['id'], link['type']))
                    for node in link['nodes']:
                        print(get_message("connection_point").format(node['label'], node['adapter'], node['port']))
            else:
                print(get_message("no_links"))
        
        return projects_info
    
    def print_project_summary(self, project_name, project_details):
        """
        打印项目摘要信息
        
        Args:
            project_name: 项目名称
            project_details: 项目详细信息
        """
        print(get_message("project_summary").format(project_name))
        print(get_message("project_id").format(project_details['id']))
        print(get_message("node_count").format(len(project_details['nodes'])))
        print(get_message("link_count").format(len(project_details['links'])))
        
        # 统计不同状态的节点
        status_count = {}
        for node in project_details['nodes']:
            status = node['status']
            status_count[status] = status_count.get(status, 0) + 1
        
        print(get_message("node_status_stats"))
        for status, count in status_count.items():
            print(get_message("status_count").format(status, count))

def main():
    """
    主函数 - 独立运行时使用
    """
    try:
        # 创建项目信息管理器，明确传递服务器URL
        project_manager = ProjectInfoManager("http://192.168.101.1:3080")
        
        # 获取所有打开项目的信息
        projects_info = project_manager.get_all_opened_projects_info()
        
        # 打印项目摘要
        print(f"\n{'='*60}")
        print("项目信息摘要")
        print(f"{'='*60}")
        
        for project_name, project_details in projects_info.items():
            project_manager.print_project_summary(project_name, project_details)
            
    except Exception as e:
        print(f"操作过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
