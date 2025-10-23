"""
GNS3 Copilot Tools Package

This package provides various tools for interacting with GNS3 network simulator, including:
- Device configuration command execution
- Display command execution
- Multiple device command execution using Nornir
- GNS3 topology reading
- Node and link management

Main modules:
- config_tools_nornir: Multiple device configuration command execution tool using Nornir
- display_tools_nornir: Multiple device command execution tool using Nornir
- gns3_topology_reader: GNS3 topology reading tool
- gns3_create_node: GNS3 node creation tool
- gns3_create_link: GNS3 link creation tool
- gns3_start_node: GNS3 node startup tool
- gns3_get_node_temp: GNS3 template retrieval tool
- custom_gns3fy: Custom GNS3 functionality module

Version: 1.0.0
Author: GNS3 Copilot Team
"""

# Import main tool classes
from .config_tools_nornir import ExecuteMultipleDeviceConfigCommands
from .display_tools_nornir import ExecuteMultipleDeviceCommands
from .gns3_topology_reader import GNS3TopologyTool
from .gns3_create_node import GNS3CreateNodeTool
from .gns3_create_link import GNS3LinkTool
from .gns3_start_node import GNS3StartNodeTool
from .gns3_get_node_temp import GNS3TemplateTool

# Package version information
__version__ = "1.0.0"
__author__ = "GNS3 Copilot Team"

# Export main tool classes
__all__ = [
    "ExecuteMultipleDeviceConfigCommands",
    "ExecuteMultipleDeviceCommands",
    "GNS3TopologyTool",
    "GNS3CreateNodeTool",
    "GNS3LinkTool",
    "GNS3StartNodeTool",
    "GNS3TemplateTool",
]

# Package initialization message
print(f"GNS3 Copilot Tools package loaded (version {__version__})")
