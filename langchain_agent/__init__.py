"""
GNS3 LangChain Agent包
提供基于LangChain的GNS3网络设备管理Agent
"""

from .agent import GNS3Agent
from .config import AgentConfig
from .tools import create_gns3_tools
from .prompts import (
    SYSTEM_PROMPT,
    OSPF_ANALYSIS_PROMPT,
    BGP_ANALYSIS_PROMPT,
    GENERAL_NETWORK_ANALYSIS_PROMPT
)

__version__ = "0.1.0"

__all__ = [
    "GNS3Agent",
    "AgentConfig", 
    "create_gns3_tools",
    "SYSTEM_PROMPT",
    "OSPF_ANALYSIS_PROMPT",
    "BGP_ANALYSIS_PROMPT",
    "GENERAL_NETWORK_ANALYSIS_PROMPT"
]