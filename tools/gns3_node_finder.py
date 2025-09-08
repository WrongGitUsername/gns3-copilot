import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import GNS3ProjectManager


class DeviceFinder:
    """
    设备查找器类，用于从GNS3项目中查找设备的project_id和node_id
    """
    
    def __init__(self, server_url: str = "http://localhost:3080", 
                 user: str = None, 
                 password: str = None,
                 detailed: bool = True):
        """
        初始化设备查找器
        
        Args:
            server_url (str): GNS3 服务器 URL
            user (str, optional): 用户名
            password (str, optional): 密码
            detailed (bool): 是否获取详细的项目信息
        """
        self.manager = GNS3ProjectManager(server_url=server_url, user=user, password=password)
        self.project_info = self.manager.get_open_projects_info(detailed=detailed)
    
    def find_device(self, device_name):
        """
        根据设备名称查找project_id和node_id
        
        Args:
            device_name (str): 设备名称，如 "R-2"
            
        Returns:
            dict: 包含project_id和node_id的字典，未找到返回None
        """
        for project in self.project_info:
            project_id = project.get('basic_info', {}).get('project_id')
            
            for node in project.get('nodes', []):
                if node.get('name') == device_name:
                    return {
                        'device_name': device_name,
                        'project_id': project_id,
                        'node_id': node.get('node_id')
                    }
        return None


# 使用示例
if __name__ == "__main__":
    # 创建设备查找器实例
    finder = DeviceFinder()
    
    # 查找 R-2 设备
    result = finder.find_device("R-3")
    print(result)