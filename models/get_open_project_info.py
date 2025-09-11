import logging
import json
from gns3fy.gns3fy import Gns3Connector, Project
from typing import List, Dict, Optional, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GNS3ProjectManager:
    """
    GNS3 项目管理器类 (重构版)
    - 使用延迟连接和缓存机制提高效率。
    - 使用 logging 模块进行日志记录。
    - 分离了数据获取与显示逻辑。
    """
    
    def __init__(self, server_url: str = "http://localhost:3080", 
                 user: Optional[str] = None, 
                 password: Optional[str] = None):
        self.server_url = server_url
        self.user = user
        self.password = password
        self._connector: Optional[Gns3Connector] = None
        self._project_cache: Optional[List[Dict[str, Any]]] = None

    @property
    def connector(self) -> Gns3Connector:
        """
        延迟连接 (Lazy Connection) 属性。
        在第一次访问时才建立与 GNS3 服务器的连接。
        """
        if self._connector is None:
            try:
                logging.info(f"正在连接到 GNS3 服务器: {self.server_url}")
                self._connector = Gns3Connector(url=self.server_url, user=self.user, cred=self.password)
                # 验证连接是否成功
                self._connector.get_version()
                logging.info("✅ GNS3 服务器连接成功")
            except Exception as e:
                logging.error(f"❌ 连接 GNS3 服务器失败: {e}")
                raise ConnectionError(f"无法连接到 GNS3 服务器: {e}") from e
        return self._connector

    def refresh(self):
        """清空本地缓存，强制下次调用时从服务器重新获取数据。"""
        logging.info("项目缓存已清空。")
        self._project_cache = None

    def get_open_projects_info(self, detailed: bool = True) -> List[Dict]:
        """
        获取所有打开项目的信息。

        该方法会使用缓存以避免不必要的网络请求。
        使用 `refresh()` 方法来强制更新。

        Args:
            detailed (bool): 是否包含节点的详细信息。

        Returns:
            List[Dict]: 打开项目的信息列表。
        """
        if self._project_cache is not None:
            logging.info("从缓存中获取项目信息。")
            return self._project_cache

        logging.info("正在从服务器获取项目信息...")
        open_projects_info = []
        try:
            projects = self.connector.get_projects()
            
            for proj_dict in projects:
                project = Project(project_id=proj_dict['project_id'], connector=self.connector)
                project.get()
                
                if project.status == 'opened':
                    project_info = {
                        "name": project.name,
                        "project_id": project.project_id,
                        "status": project.status,
                        "node_count": len(project.nodes)
                    }
                    if detailed:
                        project_info["nodes"] = [
                            {
                                "name": node.name,
                                "node_id": node.node_id,
                                "node_type": node.node_type,
                                "status": node.status,
                                "console_host": node.console_host,
                                "console_port": node.console
                            } for node in project.nodes
                        ]
                    open_projects_info.append(project_info)
            
            self._project_cache = open_projects_info
            logging.info(f"获取了 {len(open_projects_info)} 个打开的项目信息。")
            return self._project_cache
        except ConnectionError as e:
            logging.error(f"获取项目信息失败，连接错误: {e}")
            return []
        except Exception as e:
            logging.error(f"获取项目信息时发生未知错误: {e}", exc_info=True)
            return []

    def get_summary_string(self) -> str:
        """
        生成打开项目的摘要信息字符串。

        Returns:
            str: 格式化后的摘要信息。
        """
        open_projects = self.get_open_projects_info(detailed=False)
        
        if not open_projects:
            return "未找到打开的项目。"
        
        summary_lines = ["="*20 + " 打开的项目摘要 " + "="*20]
        for proj in open_projects:
            summary_lines.append(f"  - 项目: {proj['name']} (ID: {proj['project_id']})")
            summary_lines.append(f"    状态: {proj['status']}, 节点数: {proj['node_count']}")
        summary_lines.append("="*61)
        
        return "\n".join(summary_lines)

    def save_to_file(self, filename: str = "open_projects_info.json"):
        """
        将打开项目的信息保存到 JSON 文件。

        Args:
            filename (str): 要保存的文件名。
        """
        projects_info = self.get_open_projects_info(detailed=True)
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(projects_info, f, indent=4, ensure_ascii=False)
            logging.info(f"✅ 打开的项目信息已保存到 '{filename}'")
        except IOError as e:
            logging.error(f"❌ 保存文件失败: {e}")


# 为了保持向后兼容性，提供原来的函数接口
def get_open_projects_info(server_url: str = "http://localhost:3080", 
                          user: Optional[str] = None, 
                          password: Optional[str] = None,
                          detailed: bool = True) -> List[Dict]:
    try:
        manager = GNS3ProjectManager(server_url, user, password)
        return manager.get_open_projects_info(detailed)
    except ConnectionError:
        return []


def print_open_projects_summary(server_url: str = "http://localhost:3080",
                               user: Optional[str] = None,
                               password: Optional[str] = None):
    try:
        manager = GNS3ProjectManager(server_url, user, password)
        summary_string = manager.get_summary_string()
        print(summary_string)
    except ConnectionError as e:
        # The logger in the manager already printed the error
        print(f"无法打印摘要: {e}")


def save_open_projects_to_file(filename: str = "open_projects_info.json",
                              server_url: str = "http://localhost:3080",
                              user: Optional[str] = None,
                              password: Optional[str] = None):
    try:
        manager = GNS3ProjectManager(server_url, user, password)
        manager.save_to_file(filename)
    except ConnectionError as e:
        print(f"无法保存文件: {e}")


if __name__ == "__main__":
    # 使用示例
    logging.info("--- 示例 1: 打印摘要 ---")
    print_open_projects_summary()
    
    logging.info("\n--- 示例 2: 保存到文件 ---")
    save_open_projects_to_file()
    
    logging.info("\n--- 示例 3: 获取详细信息并使用缓存 ---")
    manager = GNS3ProjectManager()
    try:
        # 第一次调用，从服务器获取
        detailed_info = manager.get_open_projects_info(detailed=True)
        if detailed_info:
            print(f"获取到 {len(detailed_info)} 个项目的详细信息。")
        
        # 第二次调用，应该从缓存获取
        detailed_info_cached = manager.get_open_projects_info(detailed=True)
        if detailed_info_cached:
            print(f"再次获取，获取到 {len(detailed_info_cached)} 个项目的详细信息。")

        # 强制刷新缓存
        manager.refresh()
        detailed_info_refreshed = manager.get_open_projects_info(detailed=True)
        if detailed_info_refreshed:
            print(f"刷新后，获取到 {len(detailed_info_refreshed)} 个项目的详细信息。")

    except ConnectionError as e:
        logging.error(f"主程序运行失败: {e}")