"""
GNS3 命令执行器 (重构版)

该类通过上下文管理器 (`session`) 来管理与设备控制台的连接，
从而实现在单个连接上高效地执行多组命令。
"""

import sys
import os
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
import logging

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.gns3_web_console import GNS3WebConsole


class GNS3CommandExecutor:
    """
    GNS3 命令执行器
    提供简化的接口来执行设备命令并获取完整结果
    """
    
    def __init__(self, server_url: str = "http://localhost:3080", 
                 user: Optional[str] = None, 
                 password: Optional[str] = None):
        """
        初始化命令执行器
        
        Args:
            server_url (str): GNS3 服务器 URL
            user (str, optional): 用户名
            password (str, optional): 密码
        """
        self._console = GNS3WebConsole(server_url=server_url, user=user, password=password)
        self.server_url = server_url

    @contextmanager
    def session(self, project_id: str, node_id: str):
        """
        创建一个与特定设备的会话，作为上下文管理器。
        在会话期间，WebSocket 连接将被保持和复用。

        用法:
            with executor.session(proj_id, node_id) as device_session:
                result1 = device_session.execute(["show version"])
                result2 = device_session.execute(["show ip int brief"])
        """
        try:
            self._console.connect(project_id, node_id)
            # yield 实例自身，允许调用 execute 方法
            yield self
        finally:
            self._console.close()

    def execute(self, commands: List[str], timeout: int = 30) -> Dict[str, Any]:
        """
        在当前会话中执行一系列命令，并返回包含统计信息的详细结果。
        此方法必须在 `with executor.session(...)` 块中使用。

        Args:
            commands (List[str]): 要执行的命令列表。
            timeout (int): 每个命令的超时时间（秒）。

        Returns:
            Dict[str, Any]: 包含执行摘要和每个命令详细结果的字典。
        """
        if not self._console.is_connected():
            raise ConnectionError("连接已断开。请在 'with executor.session(...)' 上下文中使用此方法。")

        # 1. 底层执行命令
        command_results = self._console.send_commands(commands, timeout)
        
        # 2. 在上层进行统计和格式化
        total_commands = len(command_results)
        successful_commands = sum(1 for r in command_results if r['success'])
        total_execution_time = sum(r.get('execution_time', 0) for r in command_results)
        
        success_rate = (successful_commands / total_commands) * 100 if total_commands > 0 else 0
        avg_time = total_execution_time / total_commands if total_commands > 0 else 0

        # 3. 组装最终的、包含摘要的结果字典
        summary = {
            'execution_summary': {
                'total_commands': total_commands,
                'successful_commands': successful_commands,
                'failed_commands': total_commands - successful_commands,
                'success_rate': f"{success_rate:.1f}%",
                'total_execution_time': f"{total_execution_time:.2f}s",
                'average_execution_time': f"{avg_time:.2f}s",
            },
            'command_results': command_results,
            'failed_commands_details': [r for r in command_results if not r['success']],
            'all_outputs': '\n'.join([f"# Command: {r['command']}\n{r['output']}" 
                                    for r in command_results if r['success']])
        }
        
        return summary


def print_execution_summary(summary: Dict[str, Any]):
    """
    一个辅助函数，用于将 execute 方法返回的结果以用户友好的格式打印到控制台。
    """
    exec_summary = summary.get('execution_summary', {})
    
    print("\n📊 执行摘要:")
    print(f"   总命令数: {exec_summary.get('total_commands', 'N/A')}")
    print(f"   成功: {exec_summary.get('successful_commands', 'N/A')}")
    print(f"   失败: {exec_summary.get('failed_commands', 'N/A')}")
    print(f"   成功率: {exec_summary.get('success_rate', 'N/A')}")
    print(f"   总执行时间: {exec_summary.get('total_execution_time', 'N/A')}")
    
    failed_commands = summary.get('failed_commands_details', [])
    if failed_commands:
        print("\n❌ 失败的命令详情:")
        for failed in failed_commands:
            print(f"   - 命令: '{failed['command']}' - 错误: {failed.get('error', 'Unknown')}")


# 使用示例
if __name__ == '__main__':
    # 这是一个如何使用重构后代码的示例
    # 请将 project_id 和 node_id 替换为您的实际值
    PROJECT_ID = "ec1c0382-ba64-4de0-b57c-af5fdf781292"  # 示例 ID
    NODE_ID = "40f32375-7cc1-4924-b990-fb378cf80c01"     # 示例 ID
    
    commands1 = ["", "enable", "terminal length 0", "show version"]
    commands2 = ["show ip interface brief", "show running-config"]
    
    # 1. 创建一次执行器实例
    executor = GNS3CommandExecutor()
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        # 2. 使用 with 语句为特定设备创建一个会话
        print(f"--- 正在为设备 {NODE_ID[:8]} 创建会话 ---")
        with executor.session(project_id=PROJECT_ID, node_id=NODE_ID) as device_session:
            
            # 3. 在同一个会话中，可以执行多次命令，连接是复用的
            print("\n--- 第一次执行 (show version) ---")
            result1 = device_session.execute(commands1, timeout=15)
            print_execution_summary(result1)  # 使用辅助函数打印结果
            
            print("\n--- 第二次执行 (show config) ---")
            result2 = device_session.execute(commands2, timeout=20)
            print_execution_summary(result2)

            # 可以在这里继续执行更多操作...

    except ConnectionError as e:
        logging.error(f"连接或执行失败: {e}")
    except Exception as e:
        logging.error(f"发生未知错误: {e}", exc_info=True)


