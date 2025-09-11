import logging
from typing import Optional, Dict

from models.get_open_project_info import GNS3ProjectManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class DeviceFinder:
    """
    设备查找器 (重构版)

    该类现在依赖于一个 GNS3ProjectManager 实例来获取项目信息，
    从而可以利用其缓存和连接管理功能，大幅提升性能。
    """

    def __init__(self, project_manager: GNS3ProjectManager):
        """
        初始化设备查找器。

        Args:
            project_manager (GNS3ProjectManager): 一个 GNS3ProjectManager 的实例。
        """
        if not isinstance(project_manager, GNS3ProjectManager):
            raise TypeError("project_manager 必须是 GNS3ProjectManager 的一个实例")
        self.project_manager = project_manager

    def find_device_ids(self, device_name: str) -> Optional[Dict[str, str]]:
        """
        根据设备名称查找其 project_id 和 node_id。

        Args:
            device_name (str): 要查找的设备名称。

        Returns:
            Optional[Dict[str, str]]: 包含 'project_id' 和 'node_id' 的字典，如果未找到则返回 None。
        """
        logging.info(f"正在查找设备 '{device_name}'...")
        try:
            # 利用 project_manager 的缓存能力
            open_projects = self.project_manager.get_open_projects_info(detailed=True)
            
            for project in open_projects:
                for node in project.get('nodes', []):
                    if node['name'] == device_name:
                        device_info = {
                            'project_id': project['project_id'],
                            'node_id': node['node_id']
                        }
                        logging.info(f"✅ 找到设备 '{device_name}' 在项目 '{project['name']}' 中 (Node ID: {node['node_id'][:8]}...)")
                        return device_info
            
            logging.warning(f"⚠️ 未在任何打开的项目中找到名为 '{device_name}' 的设备。")
            return None
        except ConnectionError as e:
            logging.error(f"查找设备时发生连接错误: {e}")
            return None
        except Exception as e:
            logging.error(f"查找设备时发生未知错误: {e}", exc_info=True)
            return None


def find_device_ids(device_name: str, server_url: str = "http://localhost:3080", user: Optional[str] = None, password: Optional[str] = None) -> Optional[Dict[str, str]]:
    """
    一个便捷的独立函数，用于查找设备。
    为了保持向后兼容性而保留。
    """
    try:
        manager = GNS3ProjectManager(server_url, user, password)
        finder = DeviceFinder(manager)
        return finder.find_device_ids(device_name)
    except (ConnectionError, TypeError) as e:
        logging.error(f"函数 find_device_ids 运行失败: {e}")
        return None


# 使用示例
if __name__ == '__main__':
    # 这是一个如何使用重构后代码的示例
    
    # --- 推荐的使用方式：共享 Manager 实例 ---
    logging.info("\n--- 推荐用法：共享 GNS3ProjectManager 实例 ---")
    try:
        # 1. 创建一个 manager 实例，它可以在多个工具间共享
        shared_manager = GNS3ProjectManager()
        
        # 2. 将 manager 实例传递给 finder
        finder = DeviceFinder(shared_manager)
        
        # 3. 进行查找
        device_to_find = "R1"
        r1_info = finder.find_device_ids(device_to_find)
        if r1_info:
            print(f"找到 '{device_to_find}': {r1_info}")
        
        # 4. 再次查找，这次会使用缓存，速度更快
        device_to_find_2 = "R2"
        r2_info = finder.find_device_ids(device_to_find_2)
        if r2_info:
            print(f"找到 '{device_to_find_2}': {r2_info}")

        # 5. 查找一个不存在的设备
        non_existent_device = "R99"
        r99_info = finder.find_device_ids(non_existent_device)
        if not r99_info:
            print(f"未找到 '{non_existent_device}'，符合预期。")

    except ConnectionError as e:
        logging.error(f"示例运行失败: {e}")

    # --- 兼容旧用法的独立函数 ---
    logging.info("\n--- 兼容旧用法的独立函数 ---")
    device_info_func = find_device_ids("R1")
    if device_info_func:
        print(f"通过独立函数找到 'R1': {device_info_func}")