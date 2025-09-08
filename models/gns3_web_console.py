import sys
import os
import time
import json
import threading
from typing import Optional, Dict, Any, List
import requests
import websocket
from queue import Queue, Empty

# 确保 websocket 库可用
try:
    from websocket import WebSocketApp
except ImportError:
    print("错误: 请安装 websocket-client 库")
    print("运行命令: pip install websocket-client")
    sys.exit(1)

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gns3fy.gns3fy import Gns3Connector


class GNS3WebConsole:
    """
    GNS3 Web Console 命令执行器
    用于通过 WebSocket 连接到设备控制台并执行命令
    """
    
    def __init__(self, server_url: str = "http://localhost:3080", 
                 user: Optional[str] = None, 
                 password: Optional[str] = None):
        """
        初始化 GNS3 Web Console 连接器
        
        Args:
            server_url (str): GNS3 服务器 URL
            user (str, optional): 用户名
            password (str, optional): 密码
        """
        self.server_url = server_url.rstrip('/')
        self.user = user
        self.password = password
        self.connector = Gns3Connector(url=server_url, user=user, cred=password)
        
        # WebSocket 相关
        self.ws = None
        self.response_queue = Queue()
        self.is_connected = False
        self.response_buffer = ""
    
    def _get_websocket_url(self, project_id: str, node_id: str) -> str:
        """
        生成 WebSocket 连接 URL
        
        Args:
            project_id (str): 项目 ID
            node_id (str): 节点 ID
            
        Returns:
            str: WebSocket URL
        """
        ws_url = self.server_url.replace('http://', 'ws://').replace('https://', 'wss://')
        return f"{ws_url}/v2/projects/{project_id}/nodes/{node_id}/console/ws"
    
    def _on_message(self, ws, message):
        """WebSocket 消息处理回调"""
        try:
            # 解析消息
            if isinstance(message, bytes):
                message = message.decode('utf-8', errors='ignore')
            
            self.response_buffer += message
            self.response_queue.put(message)
            
        except Exception as e:
            print(f"处理消息时发生错误: {e}")
    
    def _on_error(self, ws, error):
        """WebSocket 错误处理回调"""
        print(f"WebSocket 错误: {error}")
    
    def _on_close(self, ws, close_status_code, close_msg):
        """WebSocket 关闭处理回调"""
        self.is_connected = False
        print("WebSocket 连接已关闭")
    
    def _on_open(self, ws):
        """WebSocket 连接打开回调"""
        self.is_connected = True
        print("WebSocket 连接已建立")
    
    def connect_to_console(self, project_id: str, node_id: str, timeout: int = 10) -> bool:
        """
        连接到设备控制台
        
        Args:
            project_id (str): 项目 ID
            node_id (str): 节点 ID
            timeout (int): 连接超时时间（秒）
            
        Returns:
            bool: 连接是否成功
        """
        try:
            ws_url = self._get_websocket_url(project_id, node_id)
            print(f"正在连接到: {ws_url}")
            
            # 创建 WebSocket 连接
            self.ws = websocket.WebSocketApp(
                ws_url,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close,
                on_open=self._on_open
            )
            
            # 在后台线程中运行 WebSocket
            self.ws_thread = threading.Thread(target=self.ws.run_forever)
            self.ws_thread.daemon = True
            self.ws_thread.start()
            
            # 等待连接建立
            start_time = time.time()
            while not self.is_connected and time.time() - start_time < timeout:
                time.sleep(0.1)
            
            if self.is_connected:
                # 清空初始输出
                time.sleep(1)
                self._clear_queue()
                return True
            else:
                print("连接超时")
                return False
                
        except Exception as e:
            print(f"连接失败: {e}")
            return False
    
    def _clear_queue(self):
        """清空响应队列"""
        try:
            while True:
                self.response_queue.get_nowait()
        except Empty:
            pass
        self.response_buffer = ""
    
    def send_command(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """
        发送命令到设备控制台
        
        Args:
            command (str): 要执行的命令
            timeout (int): 命令执行超时时间（秒）
            
        Returns:
            Dict[str, Any]: 命令执行结果
        """
        if not self.is_connected or not self.ws:
            return {
                'success': False,
                'error': '未连接到控制台',
                'command': command,
                'output': ''
            }
        
        try:
            self._clear_queue()
            print(f"发送命令: {repr(command)}")
            self.ws.send(command + '\r\n')
            
            output = ""
            start_time = time.time()
            last_data_time = start_time
            
            while time.time() - start_time < timeout:
                try:
                    message = self.response_queue.get(timeout=0.2)  # 增加超时时间
                    output += message
                    last_data_time = time.time()
                    
                    # 检查是否有提示符，但要确保有足够的数据
                    if len(output) > 10 and self._has_prompt(output):
                        # 再等待一小段时间确保数据完整
                        time.sleep(0.1)
                        # 检查是否还有更多数据
                        try:
                            extra_message = self.response_queue.get(timeout=0.1)
                            output += extra_message
                        except Empty:
                            pass
                        break
                        
                except Empty:
                    # 如果超过2秒没有新数据，可能命令已完成
                    if time.time() - last_data_time > 2:
                        break
                    continue
            
            return {
                'success': True,
                'error': None,
                'command': command,
                'output': output.strip(),
                'execution_time': time.time() - start_time
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'command': command,
                'output': ''
            }
    
    def _has_prompt(self, output: str) -> bool:
        """
        检查输出中是否包含提示符
        更严格的判断逻辑
        """
        if not output:
            return False
        
        lines = output.split('\n')
        if len(lines) < 2:
            return False
        
        # 检查最后一行
        last_line = lines[-1].strip()
        
        # 提示符模式：以设备名开头，以#或>结尾
        import re
        prompt_patterns = [
            r'.*[#>]\s*$',  # 以#或>结尾
            r'R\d+[#>]\s*$',  # 路由器提示符
            r'Switch[#>]\s*$',  # 交换机提示符
        ]
        
        for pattern in prompt_patterns:
            if re.match(pattern, last_line):
                return True
        
        return False
    
    def execute_commands(self, project_id: str, node_id: str, commands: List[str], 
                        timeout: int = 30) -> List[Dict[str, Any]]:
        results = []
        
        # 连接到控制台
        if not self.connect_to_console(project_id, node_id):
            error_result = {
                'success': False,
                'error': '无法连接到设备控制台',
                'command': '',
                'output': ''
            }
            return [error_result] * len(commands)
        
        try:
            # 执行每个命令
            for i, command in enumerate(commands):
                print(f"执行命令 {i+1}/{len(commands)}: {command}")
                result = self.send_command(command, timeout)
                results.append(result)
                
                # 如果命令失败，记录但继续执行
                if not result['success']:
                    print(f"命令执行失败: {command} - {result.get('error', '未知错误')}")
                
                # 对于最后一个命令，增加额外的等待时间
                if i == len(commands) - 1:
                    print("等待最后一个命令完成...")
                    time.sleep(1)  # 给最后一个命令更多时间
            
            return results
            
        finally:
            # 确保在断开前有足够的时间处理最后的响应
            time.sleep(0.5)
            self.disconnect()
            
    def disconnect(self):
        """断开控制台连接"""
        if self.ws:
            try:
                self.ws.close()
                self.is_connected = False
                print("已断开控制台连接")
            except Exception as e:
                print(f"断开连接时发生错误: {e}")
    
    def get_device_info(self, project_id: str, node_id: str) -> Optional[Dict[str, Any]]:
        """
        获取设备信息
        
        Args:
            project_id (str): 项目 ID
            node_id (str): 节点 ID
            
        Returns:
            Dict[str, Any]: 设备信息
        """
        try:
            url = f"{self.server_url}/v2/projects/{project_id}/nodes/{node_id}"
            response = self.connector.http_call("GET", url)
            return response
        except Exception as e:
            print(f"获取设备信息失败: {e}")
            return None


# 使用示例
if __name__ == "__main__":
    # 创建控制台实例
    console = GNS3WebConsole()
    
    # 示例项目和节点 ID（请替换为实际值）
    project_id = "f2f7ed27-7aa3-4b11-a64c-da947a2c7210"
    node_id = "5f875fef-f795-4f06-96b2-9c34a66a296d"
    
    # 执行多个命令，使用 # 号判断完成
    commands = [
        "\r\n",                        # 发送空行唤醒
        "\r\n",
        "\r\n",
        "\r\n",
        "enable",                  # 进入特权模式
        "terminal length 0",       # 设置终端长度
        "show version",           # 显示版本
        "show ip interface brief", # 显示接口状态
        "show run",
        #"show memory summary",
    ]
    
    print("🚀 执行命令序列（基于 # 提示符判断完成）:")
    results = console.execute_commands(project_id, node_id, commands)
    
    # 在每个命令后打印调试信息
    for i, result in enumerate(results):
        print(f"\n命令 {i+3}: {result['command']}")
        print(f"输出长度: {len(result['output'])} 字符")
        print(f"最后100字符: {result['output'][-100:]}")
