"""
GNS3 模型模块
包含与 GNS3 服务器交互的相关类和函数

使用示例:
    from models import GNS3ProjectManager
    
    # 创建项目管理器
    manager = GNS3ProjectManager()
    
    # 获取打开的项目信息
    projects = manager.get_open_projects_info()
    
    # 打印项目摘要
    manager.print_open_projects_summary()
"""

from .get_open_project_info import (
    GNS3ProjectManager,
    get_open_projects_info,
    print_open_projects_summary,
    save_open_projects_to_file
)

# 导出的公共接口
__all__ = [
    'GNS3ProjectManager',
    'get_open_projects_info', 
    'print_open_projects_summary',
    'save_open_projects_to_file'
]

# 模块元信息
__version__ = '1.0.0'
__author__ = 'yueguobin'
__description__ = 'GNS3 项目管理和设备查找模块'

# 便捷别名
ProjectManager = GNS3ProjectManager
