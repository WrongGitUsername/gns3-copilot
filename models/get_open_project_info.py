import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gns3fy.gns3fy import Gns3Connector, Project
import json
from typing import List, Dict, Optional


class GNS3ProjectManager:
    """
    GNS3 项目管理器类，用于获取和管理 GNS3 服务器中的项目信息
    """
    
    def __init__(self, server_url: str = "http://localhost:3080", 
                 user: Optional[str] = None, 
                 password: Optional[str] = None):
        """
        初始化 GNS3 项目管理器
        
        Args:
            server_url (str): GNS3 服务器 URL，默认为 http://localhost:3080
            user (str, optional): 用户名（如果需要认证）
            password (str, optional): 密码（如果需要认证）
        """
        self.server_url = server_url
        self.user = user
        self.password = password
        self.connector = None
        self._connect()
    
    def _connect(self):
        """建立与 GNS3 服务器的连接"""
        try:
            self.connector = Gns3Connector(url=self.server_url, user=self.user, cred=self.password)
        except Exception as e:
            print(f"连接 GNS3 服务器时发生错误: {str(e)}")
            raise
    
    def get_open_projects_info(self, detailed: bool = True) -> List[Dict]:
        """
        获取 GNS3 服务器中所有打开状态的项目信息
        
        Args:
            detailed (bool): 是否获取详细信息（包括节点和链路信息）
            
        Returns:
            List[Dict]: 打开状态的项目信息列表
        """
        try:
            # 获取所有项目
            all_projects = self.connector.get_projects()
            
            # 筛选出打开状态的项目
            open_projects = [project for project in all_projects if project.get('status') == 'opened']
            
            if not detailed:
                return open_projects
            
            # 获取详细信息
            detailed_projects = []
            for project_data in open_projects:
                project = Project(
                    project_id=project_data['project_id'],
                    connector=self.connector
                )
                
                # 获取项目详细信息
                project.get(get_links=True, get_nodes=True, get_stats=True)
                
                # 构建详细信息字典
                project_info = {
                    'basic_info': {
                        'name': project.name,
                        'project_id': project.project_id,
                        'status': project.status,
                        'path': project.path,
                        'filename': project.filename,
                        'auto_start': project.auto_start,
                        'auto_close': project.auto_close,
                        'scene_width': project.scene_width,
                        'scene_height': project.scene_height,
                        'show_grid': project.show_grid,
                        'show_interface_labels': project.show_interface_labels,
                        'snap_to_grid': project.snap_to_grid,
                    },
                    'statistics': project.stats if project.stats else {},
                    'nodes': [],
                    'links': [],
                    'nodes_summary': project.nodes_summary(is_print=False) if project.nodes else [],
                    'links_summary': project.links_summary(is_print=False) if project.links else []
                }
                
                # 添加节点详细信息
                if project.nodes:
                    for node in project.nodes:
                        node_info = {
                            'name': node.name,
                            'node_id': node.node_id,
                            'node_type': node.node_type,
                            'status': node.status,
                            'console': node.console,
                            'console_type': node.console_type,
                            'console_host': node.console_host,
                            'x': node.x,
                            'y': node.y,
                            'z': node.z,
                            'symbol': node.symbol,
                            'template': node.template,
                            'locked': node.locked,
                            'properties': node.properties
                        }
                        project_info['nodes'].append(node_info)
                
                # 添加链路详细信息
                if project.links:
                    for link in project.links:
                        link_info = {
                            'link_id': link.link_id,
                            'link_type': link.link_type,
                            'nodes': link.nodes,
                            'suspend': link.suspend,
                            'capturing': link.capturing,
                            'filters': link.filters
                        }
                        project_info['links'].append(link_info)
                
                detailed_projects.append(project_info)
            
            return detailed_projects
            
        except Exception as e:
            print(f"获取项目信息时发生错误: {str(e)}")
            return []
    
    def print_open_projects_summary(self):
        """打印打开状态项目的摘要信息"""
        try:
            # 获取所有项目
            all_projects = self.connector.get_projects()
            open_projects = [p for p in all_projects if p.get('status') == 'opened']
            
            if not open_projects:
                print("当前没有打开的项目")
                return
            
            print(f"\n=== GNS3 服务器打开状态的项目 (共 {len(open_projects)} 个) ===\n")
            
            for i, project_data in enumerate(open_projects, 1):
                project = Project(project_id=project_data['project_id'], connector=self.connector)
                project.get(get_stats=True)
                
                print(f"{i}. 项目名称: {project.name}")
                print(f"   项目 ID: {project.project_id}")
                print(f"   状态: {project.status}")
                print(f"   路径: {project.path}")
                
                if project.stats:
                    print(f"   统计信息:")
                    print(f"     - 节点数量: {project.stats.get('nodes', 0)}")
                    print(f"     - 链路数量: {project.stats.get('links', 0)}")
                    print(f"     - 绘图数量: {project.stats.get('drawings', 0)}")
                    print(f"     - 快照数量: {project.stats.get('snapshots', 0)}")
                
                # 获取节点摘要
                nodes_summary = project.nodes_summary(is_print=False)
                if nodes_summary:
                    print(f"   节点信息:")
                    for node_name, node_status, console_port, node_id in nodes_summary[:5]:  # 只显示前5个
                        print(f"     - {node_name}: {node_status} (控制台: {console_port})")
                    if len(nodes_summary) > 5:
                        print(f"     ... 还有 {len(nodes_summary) - 5} 个节点")
                
                print("-" * 60)
            
        except Exception as e:
            print(f"获取项目摘要时发生错误: {str(e)}")
    
    def save_open_projects_to_file(self, filename: str = "open_projects_info.json"):
        """
        将打开状态的项目信息保存到 JSON 文件
        
        Args:
            filename (str): 保存的文件名
        """
        try:
            projects_info = self.get_open_projects_info(detailed=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(projects_info, f, ensure_ascii=False, indent=2)
            
            print(f"项目信息已保存到文件: {filename}")
            print(f"共保存了 {len(projects_info)} 个打开状态的项目信息")
            
        except Exception as e:
            print(f"保存项目信息时发生错误: {str(e)}")


# 为了保持向后兼容性，提供原来的函数接口
def get_open_projects_info(server_url: str = "http://localhost:3080", 
                          user: Optional[str] = None, 
                          password: Optional[str] = None,
                          detailed: bool = True) -> List[Dict]:
    """
    获取 GNS3 服务器中所有打开状态的项目信息（向后兼容函数）
    """
    manager = GNS3ProjectManager(server_url=server_url, user=user, password=password)
    return manager.get_open_projects_info(detailed=detailed)


def print_open_projects_summary(server_url: str = "http://localhost:3080",
                               user: Optional[str] = None,
                               password: Optional[str] = None):
    """
    打印打开状态项目的摘要信息（向后兼容函数）
    """
    manager = GNS3ProjectManager(server_url=server_url, user=user, password=password)
    manager.print_open_projects_summary()


def save_open_projects_to_file(filename: str = "open_projects_info.json",
                              server_url: str = "http://localhost:3080",
                              user: Optional[str] = None,
                              password: Optional[str] = None):
    """
    将打开状态的项目信息保存到 JSON 文件（向后兼容函数）
    """
    manager = GNS3ProjectManager(server_url=server_url, user=user, password=password)
    manager.save_open_projects_to_file(filename=filename)


if __name__ == "__main__":
    # 示例用法 - 使用类的方式
    print("获取 GNS3 服务器打开状态的项目信息...")
    
    # 创建项目管理器实例
    manager = GNS3ProjectManager()
    
    # 打印摘要信息
    manager.print_open_projects_summary()
    
    # 获取详细信息
    open_projects = manager.get_open_projects_info(detailed=True)
    
    if open_projects:
        print(f"\n找到 {len(open_projects)} 个打开状态的项目")
        
        # 保存到文件
        manager.save_open_projects_to_file()
        
        # 显示第一个项目的详细信息示例
        if open_projects:
            first_project = open_projects[0]
            print(f"\n第一个项目详细信息示例:")
            print(f"项目名称: {first_project['basic_info']['name']}")
            print(f"节点数量: {len(first_project['nodes'])}")
            print(f"链路数量: {len(first_project['links'])}")
    else:
        print("当前没有打开的项目")