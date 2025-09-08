"""
LangChain Agent配置文件
"""

import os
from typing import Optional

class AgentConfig:
    """Agent配置类"""
    
    # GNS3服务器配置
    GNS3_SERVER_URL: str = "http://localhost:3080"
    GNS3_USER: Optional[str] = None
    GNS3_PASSWORD: Optional[str] = None
    
    # LLM配置
    LLM_MODEL: str = "deepseek-chat"
    LLM_TEMPERATURE: float = 0.1
    
    # DeepSeek配置
    DEEPSEEK_API_KEY: Optional[str] = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_BASE_URL: Optional[str] = os.getenv("DEEPSEEK_BASE_URL")  # DeepSeek固定端点
    
    # Agent配置
    MAX_ITERATIONS: int = 10
    COMMAND_TIMEOUT: int = 30
    
    # 支持的网络协议命令
    PROTOCOL_COMMANDS = {
        "ospf": [
            "show ip ospf",
            "show ip ospf neighbor",
            "show ip ospf database",
            "show ip route ospf"
        ],
        "bgp": [
            "show ip bgp",
            "show ip bgp summary",
            "show ip bgp neighbors"
        ],
        "eigrp": [
            "show ip eigrp neighbors",
            "show ip eigrp topology",
            "show ip route eigrp"
        ],
        "interface": [
            "show ip interface brief",
            "show interfaces"
        ],
        "route": [
            "show ip route",
            "show ip route summary"
        ]
    }
    
    @classmethod
    def get_protocol_commands(cls, protocol: str) -> list:
        """获取指定协议的命令列表"""
        return cls.PROTOCOL_COMMANDS.get(protocol.lower(), [])
    
    @classmethod
    def get_all_protocols(cls) -> list:
        """获取所有支持的协议列表"""
        return list(cls.PROTOCOL_COMMANDS.keys())
