import logging
import re
import time
import threading
import queue
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

import websocket
from gns3fy import Gns3Connector

# 1. 使用 logging 模块替换 print
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 2. 将魔法数字定义为常量
PROMPT_REGEX = re.compile(r"(\r\n|^\s*)([a-zA-Z0-9.\-_\s()]+[>#])\s*$")
CONNECT_TIMEOUT_SECONDS = 10
COMMAND_INACTIVITY_TIMEOUT_SECONDS = 0.2  # 在看到输出后，等待这么久没有新数据就认为命令结束
DEFAULT_COMMAND_TIMEOUT_SECONDS = 30


class GNS3WebConsole:
    """
    通过 WebSocket 与 GNS3 节点的控制台进行交互。

    该类被重构为上下文管理器，以实现高效的连接复用和安全的资源管理。
    """

    def __init__(self, server_url: str = "http://localhost:3080", user: Optional[str] = None, password: Optional[str] = None):
        self.server_url = server_url
        self.user = user
        self.password = password
        
        self._ws_app = None
        self._ws_thread = None
        self._message_queue = queue.Queue()
        
        # 3. 使用 threading.Event 进行线程同步
        self._connected_event = threading.Event()
        self._connection_failed_event = threading.Event()
        self._connection_error = None

    def __enter__(self):
        """上下文管理器入口：返回实例自身"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口：确保连接被关闭"""
        self.close()

    def is_connected(self) -> bool:
        """检查 WebSocket 是否处于连接状态"""
        return self._connected_event.is_set()

    def connect(self, project_id: str, node_id: str):
        """
        建立与指定节点控制台的 WebSocket 连接。
        该方法会阻塞直到连接成功或超时。
        """
        if self.is_connected():
            logging.info("连接已建立，无需重复连接。")
            return

        # 使用 Gns3Connector 主要是为了获取认证头（如果需要）
        # 注意：这里的 `cred` 参数是根据用户本地的 gns3fy.py 调整的
        connector = Gns3Connector(url=self.server_url, user=self.user, cred=self.password)
        
        # 正确构建 WebSocket URL
        parsed_url = urlparse(self.server_url)
        ws_scheme = 'wss' if parsed_url.scheme == 'https' else 'ws'
        # GNS3 的 WebSocket 控制台路径 (根据用户提供的精确格式)
        ws_path = f"/v2/projects/{project_id}/nodes/{node_id}/console/ws"
        console_url = f"{ws_scheme}://{parsed_url.netloc}{ws_path}"
        
        # 手动构建认证头 (根据用户本地 gns3fy 版本进行调整)
        auth_header = {}
        if self.user and self.password:
            import base64
            credentials = f"{self.user}:{self.password}".encode("utf-8")
            encoded_credentials = base64.b64encode(credentials).decode("utf-8")
            auth_header["Authorization"] = f"Basic {encoded_credentials}"

        self._ws_app = websocket.WebSocketApp(
            console_url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            header=auth_header
        )

        self._ws_thread = threading.Thread(target=self._ws_app.run_forever, daemon=True)
        self._ws_thread.start()

        logging.info(f"正在连接到 {console_url}...")
        
        # 等待连接成功或失败
        connection_established = self._connected_event.wait(timeout=CONNECT_TIMEOUT_SECONDS)
        
        if self._connection_failed_event.is_set():
            raise ConnectionError(f"连接失败: {self._connection_error}")
        
        if not connection_established:
            self.close()
            raise TimeoutError(f"连接到 {console_url} 超时。")
            
        logging.info("连接成功。")

    def close(self):
        """关闭 WebSocket 连接和线程"""
        if self._ws_app:
            self._ws_app.close()
            self._ws_app = None
        if self._ws_thread and self._ws_thread.is_alive():
            self._ws_thread.join(timeout=2)
        
        # 重置所有事件和状态
        self._connected_event.clear()
        self._connection_failed_event.clear()
        self._connection_error = None
        # 清空队列
        while not self._message_queue.empty():
            self._message_queue.get_nowait()
            
        logging.info("连接已关闭。")

    def send_commands(self, commands: List[str], timeout: int = DEFAULT_COMMAND_TIMEOUT_SECONDS) -> Dict[str, str]:
        """
        发送一系列命令并收集它们的输出。

        Args:
            commands: 要执行的命令列表。
            timeout: 每个命令的执行超时时间。

        Returns:
            一个字典，键是命令，值是该命令的输出。
        """
        if not self.is_connected():
            raise ConnectionError("WebSocket 未连接。请先调用 connect()。")

        results = {}
        # 先清空一次队列，确保拿到的是干净的prompt
        self._clear_queue_and_read_until_prompt()

        for command in commands:
            logging.info(f"执行命令: {command}")
            self._ws_app.send(command + "\r\n")
            
            output = self._read_until_prompt(timeout=timeout)
            
            # 清理输出，移除命令本身和末尾的提示符
            clean_output = re.sub(r'^' + re.escape(command) + r'\r\n', '', output, 1)
            clean_output = PROMPT_REGEX.sub('', clean_output).strip()
            
            results[command] = clean_output
            logging.info(f"命令 '{command}' 的输出:\n{clean_output}")

        return results

    def _read_until_prompt(self, timeout: int = DEFAULT_COMMAND_TIMEOUT_SECONDS) -> str:
        """
        从队列中读取数据，直到检测到命令提示符或超时。
        """
        output = ""
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                # 设置一个短的超时时间，以便能频繁检查整体超时
                data = self._message_queue.get(timeout=COMMAND_INACTIVITY_TIMEOUT_SECONDS)
                output += data
                if PROMPT_REGEX.search(output):
                    logging.debug("检测到提示符，命令输出结束。")
                    return output
            except queue.Empty:
                # 如果在 COMMAND_INACTIVITY_TIMEOUT_SECONDS 内没有新数据，
                # 并且已经收到过一些数据，那么也认为命令结束了。
                if output:
                    logging.debug("在不活动超时后，认为命令输出结束。")
                    return output
        
        raise TimeoutError("读取命令输出超时。")

    def _clear_queue_and_read_until_prompt(self):
        """清空消息队列并持续读取，直到出现一个提示符，以同步控制台状态。"""
        # 先清空
        while not self._message_queue.empty():
            self._message_queue.get_nowait()
        # 再读取
        try:
            self._read_until_prompt(timeout=5)
        except TimeoutError:
            logging.warning("在同步控制台状态时未能找到初始提示符。")


    def _on_message(self, ws, message):
        """WebSocket 消息回调：将消息放入队列"""
        decoded_message = message.decode('utf-8', errors='ignore')
        logging.debug(f"收到消息: {repr(decoded_message)}")
        self._message_queue.put(decoded_message)

    def _on_error(self, ws, error):
        """WebSocket 错误回调：记录错误并设置失败事件"""
        logging.error(f"WebSocket 错误: {error}")
        self._connection_error = str(error)
        self._connection_failed_event.set()

    def _on_close(self, ws, close_status_code, close_msg):
        """WebSocket 关闭回调：记录日志并清除连接事件"""
        logging.info(f"WebSocket 连接已关闭。状态码: {close_status_code}, 消息: {close_msg}")
        self._connected_event.clear()

    def _on_open(self, ws):
        """WebSocket 打开回调：记录日志并设置连接成功事件"""
        logging.info("WebSocket on_open 回调触发。")
        self._connected_event.set()
        self._connection_failed_event.clear()

# 主执行块，用于演示和测试
if __name__ == '__main__':
    # 这是一个示例，请根据您的 GNS3 环境进行调整
    GNS3_SERVER_URL = "http://localhost:3080"
    # 如果您的 GNS3 服务器需要认证
    # GNS3_USER = "admin"
    # GNS3_PASSWORD = "password"

    # 假设我们已经知道要操作的设备信息
    # 您需要替换为您的真实 project_id 和 node_id
    # 您可以通过 get_open_project_info.py 脚本获取这些信息
    TARGET_PROJECT_ID = "ec1c0382-ba64-4de0-b57c-af5fdf781292"  # 示例 ID
    TARGET_NODE_ID = "40f32375-7cc1-4924-b990-fb378cf80c01"       # 示例 ID
    
    # 要在设备上执行的命令
    commands_to_execute = [
        "",
        "",
        "enable",
        "terminal length 0",
        "show ip interface brief",
        "show version"
    ]

    try:
        # 使用上下文管理器确保连接正确关闭
        with GNS3WebConsole(server_url=GNS3_SERVER_URL) as console:
            print(f"正在连接到项目 {TARGET_PROJECT_ID} 的节点 {TARGET_NODE_ID}...")
            console.connect(project_id=TARGET_PROJECT_ID, node_id=TARGET_NODE_ID)
            
            print("\n连接成功！正在执行命令...")
            results = console.send_commands(commands_to_execute)
            
            print("\n--- 命令执行结果 ---")
            for command, output in results.items():
                print(f"\n>> 命令: {command}\n-- 输出:\n{output}")
            print("\n--------------------")

    except (ConnectionError, TimeoutError) as e:
        print(f"\n发生错误: {e}")
    except Exception as e:
        print(f"\n发生未知错误: {e}")

    print("\n脚本执行完毕。")
