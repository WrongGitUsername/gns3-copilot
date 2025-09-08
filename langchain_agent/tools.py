"""
LangChain Tools包装器
将现有的GNS3工具包装成LangChain Tools
"""

import sys
import os
from typing import List, Dict, Any, Optional, Type
from pydantic import BaseModel, Field

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.tools import BaseTool
from tools.gns3_node_finder import DeviceFinder
from tools.gns3_command_executor import GNS3CommandExecutor
from langchain_agent.config import AgentConfig


class DeviceFinderInput(BaseModel):
    """设备查找器输入Schema"""
    device_name: str = Field(description="要查找的设备名称，例如 'R-1', 'R-2', 'SW-1' 等")


class CommandExecutorInput(BaseModel):
    """命令执行器输入Schema"""
    project_id: str = Field(description="GNS3项目ID")
    node_id: str = Field(description="设备节点ID")
    commands: List[str] = Field(description="要执行的命令列表，例如 ['show ip ospf', 'show ip ospf neighbor']")
    timeout: int = Field(default=30, description="命令执行超时时间（秒）")


class DeviceFinderTool(BaseTool):
    """设备查找工具"""
    name: str = "find_device"
    description: str = """
    根据设备名称查找GNS3项目中的设备信息。
    输入设备名称（如 'R-1', 'R-2', 'SW-1'），返回包含project_id和node_id的信息。
    这是执行设备命令前的必要步骤。
    """
    args_schema: Type[BaseModel] = DeviceFinderInput
    
    def __init__(self, server_url: str = None, user: str = None, password: str = None):
        super().__init__()
        self._server_url = server_url or AgentConfig.GNS3_SERVER_URL
        self._user = user or AgentConfig.GNS3_USER
        self._password = password or AgentConfig.GNS3_PASSWORD
        self._device_finder = None
    
    @property
    def device_finder(self):
        """延迟初始化设备查找器"""
        if self._device_finder is None:
            self._device_finder = DeviceFinder(
                server_url=self._server_url,
                user=self._user,
                password=self._password
            )
        return self._device_finder
    
    def _run(self, device_name: str) -> Dict[str, Any]:
        """执行设备查找"""
        try:
            result = self.device_finder.find_device(device_name)
            
            if result:
                return {
                    "success": True,
                    "device_info": result,
                    "message": f"成功找到设备 {device_name}"
                }
            else:
                # 获取可用设备列表
                available_devices = self._get_available_devices()
                return {
                    "success": False,
                    "error": f"未找到设备 {device_name}",
                    "available_devices": available_devices,
                    "message": f"设备 {device_name} 不存在，可用设备: {', '.join(available_devices)}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"查找设备 {device_name} 时发生错误: {str(e)}"
            }
    
    def _get_available_devices(self) -> List[str]:
        """获取可用设备列表"""
        try:
            devices = []
            for project in self.device_finder.project_info:
                for node in project.get('nodes', []):
                    device_name = node.get('name')
                    if device_name:
                        devices.append(device_name)
            return devices
        except:
            return []


class CommandExecutorTool(BaseTool):
    """命令执行工具"""
    name: str = "execute_commands"
    description: str = """
    在指定的GNS3设备上执行网络命令。
    需要project_id、node_id和命令列表。
    支持OSPF、BGP、EIGRP等网络协议命令。
    返回命令的执行结果。
    """
    args_schema: Type[BaseModel] = CommandExecutorInput
    
    def __init__(self, server_url: str = None, user: str = None, password: str = None):
        super().__init__()
        self._server_url = server_url or AgentConfig.GNS3_SERVER_URL
        self._user = user or AgentConfig.GNS3_USER
        self._password = password or AgentConfig.GNS3_PASSWORD
        self._executor = None
    
    @property
    def executor(self):
        """延迟初始化命令执行器"""
        if self._executor is None:
            self._executor = GNS3CommandExecutor(
                server_url=self._server_url,
                user=self._user,
                password=self._password
            )
        return self._executor
    
    def _run(self, project_id: str, node_id: str, commands: List[str], timeout: int = 30) -> Dict[str, Any]:
        """执行命令"""
        try:
            results = self.executor.execute_multiple_commands(
                project_id=project_id,
                node_id=node_id,
                commands=commands,
                timeout=timeout
            )
            
            return {
                "success": True,
                "results": results,
                "message": f"成功执行 {len(commands)} 个命令"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"执行命令时发生错误: {str(e)}"
            }


class ProtocolCommandSuggestionTool(BaseTool):
    """协议命令建议工具"""
    name: str = "suggest_protocol_commands"
    description: str = """
    根据协议类型建议相关的网络命令。
    输入协议名称（如 'ospf', 'bgp', 'eigrp'），返回建议的命令列表。
    """
    
    def _run(self, protocol: str) -> Dict[str, Any]:
        """建议协议命令"""
        protocol = protocol.lower()
        commands = AgentConfig.get_protocol_commands(protocol)
        
        if commands:
            return {
                "success": True,
                "protocol": protocol,
                "commands": commands,
                "message": f"为协议 {protocol} 找到 {len(commands)} 个建议命令"
            }
        else:
            available_protocols = AgentConfig.get_all_protocols()
            return {
                "success": False,
                "error": f"不支持的协议 {protocol}",
                "available_protocols": available_protocols,
                "message": f"协议 {protocol} 不支持，可用协议: {', '.join(available_protocols)}"
            }


def create_gns3_tools(server_url: str = None, user: str = None, password: str = None) -> List[BaseTool]:
    """创建GNS3工具集合"""
    return [
        DeviceFinderTool(server_url=server_url, user=user, password=password),
        CommandExecutorTool(server_url=server_url, user=user, password=password),
        ProtocolCommandSuggestionTool()
    ]
