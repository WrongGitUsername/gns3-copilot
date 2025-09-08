"""
GNS3 工具模块
包含用于 GNS3 设备查找和命令执行的工具类

模块列表:
- DeviceFinder: 设备查找器，用于通过设备名称查找 project_id 和 node_id
- GNS3CommandExecutor: GNS3 命令执行器，用于执行设备命令并返回完整结果

使用示例:
    from tools import DeviceFinder, GNS3CommandExecutor
    
    # 查找设备
    finder = DeviceFinder()
    device_info = finder.find_device("R-2")
    
    # 执行命令
    executor = GNS3CommandExecutor()
    result = executor.execute_multiple_commands(project_id, node_id, ["show version"])
"""

from .gns3_node_finder import DeviceFinder
from .gns3_command_executor import GNS3CommandExecutor, execute_commands

# 导出的公共接口
__all__ = [
    'DeviceFinder',
    'GNS3CommandExecutor',
    'execute_commands'
]

# 模块元信息
__version__ = '1.0.0'
__author__ = 'yueguobin'
__description__ = 'GNS3 工具模块'

# 便捷别名
NodeFinder = DeviceFinder
CommandExecutor = GNS3CommandExecutor