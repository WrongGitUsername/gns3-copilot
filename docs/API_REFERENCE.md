# GNS3 Copilot API Reference

This document provides detailed API documentation for all tools and modules in the GNS3 Copilot project.

## Core Tools

### GNS3TopologyTool
**Location**: `tools/gns3_topology_reader.py`

Retrieves the topology of the currently open GNS3 project.

#### Main Methods
- `_run(tool_input=None, run_manager=None) -> dict`

**Function**: Retrieves topology information for the current GNS3 project
**Returns**: Dictionary containing project ID, name, status, nodes, and links information

---

### ExecuteMultipleDeviceCommands
**Location**: `tools/display_tools_nornir.py`

Executes display commands on multiple devices concurrently using Nornir framework.

#### Main Methods
- `_run(device_names, commands, run_manager=None) -> dict`

**Function**: Executes display commands on multiple network devices simultaneously
**Parameters**: 
- `device_names` (list): List of device names
- `commands` (list): List of commands to execute

**Features**: 
- Up to 10 devices concurrent execution
- Automatic device discovery from GNS3 topology
- Comprehensive error handling

**Supported Devices**: Cisco IOSv (primary support, telnet console)

---

### ExecuteMultipleDeviceConfigCommands
**Location**: `tools/config_tools_nornir.py`

Executes configuration commands on multiple devices concurrently using Nornir framework.

#### Main Methods
- `_run(device_configs, run_manager=None) -> dict`

**Function**: Applies configuration commands to multiple network devices simultaneously
**Parameters**: 
- `device_configs` (list): List of dictionaries containing device names and config commands

**Safety Features**: 
- Command validation to prevent dangerous operations
- Rollback capability on configuration failures
- Detailed logging of all configuration changes

---

### GNS3CreateNodeTool
**Location**: `tools/gns3_create_node.py`

Creates new nodes in GNS3 projects.

#### Main Methods
- `_run(node_name, node_template, run_manager=None) -> dict`

**Function**: Creates a new node in the current GNS3 project
**Parameters**:
- `node_name` (str): Name for the new node
- `node_template` (str): Template name for the node type

---

### GNS3LinkTool
**Location**: `tools/gns3_create_link.py`

Creates links between nodes in GNS3 projects.

#### Main Methods
- `_run(node1, port1, node2, port2, run_manager=None) -> dict`

**Function**: Creates a network link between two nodes
**Parameters**:
- `node1`, `node2` (str): Node names
- `port1`, `port2` (str): Port names

---

### GNS3StartNodeTool
**Location**: `tools/gns3_start_node.py`

Controls the power state of GNS3 nodes.

#### Main Methods
- `_run(node_name, action, run_manager=None) -> dict`

**Function**: Starts, stops, or restarts a GNS3 node
**Parameters**:
- `node_name` (str): Name of the node to control
- `action` (str): Action to perform ("start", "stop", "restart")

---

### GNS3TemplateTool
**Location**: `tools/gns3_get_node_temp.py`

Retrieves available node templates from GNS3 server.

#### Main Methods
- `_run(tool_input=None, run_manager=None) -> dict`

**Function**: Gets list of available node templates for creating new nodes

---

## Process Analyzer

### LearningDocumentationCallback
**Location**: `process_analyzer/process_callback.py`

Core callback handler for capturing and documenting execution processes.

#### Main Methods
- `start_new_session(user_input) -> str`: Start new documentation session
- `record_complete_step(thought, tool_name, action_input) -> None`: Record complete ReAct execution step
- `add_observation_to_current_step(observation) -> None`: Add tool result
- `record_final_answer(answer) -> None`: Record final answer
- `finalize_session() -> dict`: Complete session and return session data
- `emergency_save(reason) -> None`: Save during interruption

---

### LearningLangChainCallback
**Location**: `process_analyzer/langchain_callback.py`

LangChain callback handler for automatic process capture.

#### Main Methods
- `on_agent_action(action, **kwargs) -> None`: Called when agent performs an action
- `on_tool_end(output, **kwargs) -> None`: Called when a tool finishes execution
- `on_agent_finish(finish, **kwargs) -> None`: Called when agent finishes execution
- `on_agent_error(error, **kwargs) -> None`: Called when an error occurs during agent execution

---

## Utility Modules

### Logging Configuration
**Location**: `tools/logging_config.py`

Provides centralized logging configuration for all tools.

#### Main Functions
- `setup_tool_logger(tool_name, log_file=None) -> logging.Logger`

**Function**: Sets up a configured logger for a specific tool
**Features**: 
- Automatic log file creation in `log/` directory
- Structured logging with timestamps
- Different log levels for development and production
- Log rotation to prevent disk space issues

---

### Custom GNS3fy
**Location**: `tools/custom_gns3fy.py`

Custom GNS3 API adapter with enhanced functionality.

#### Main Classes
- `Gns3Connector`: Enhanced GNS3 server connector with error handling and retry logic
- `Project`: GNS3 project management with additional utility methods

**Key Methods**:
- `nodes_inventory()`: Get detailed node inventory
- `links_summary()`: Get formatted link summary
- `get_console_ports()`: Extract console port information

---

## Configuration

### Environment Variables
```env
DEEPSEEK_API_KEY=your_api_key_here  # Optional: For enhanced AI capabilities
GNS3_SERVER_URL=http://localhost:3080  # GNS3 server URL
LOG_LEVEL=INFO  # Logging level (DEBUG, INFO, WARNING, ERROR)
```

### GNS3 Server Configuration
- **Default URL**: `http://localhost:3080`
- **Authentication**: None required for local development
- **Project Management**: Automatic project discovery
- **Port Allocation**: Dynamic port assignment for console connections

### Logging Configuration
- **Log Directory**: `log/`
- **Log Files**: Separate files for each tool and component
- **Log Rotation**: Automatic cleanup of old logs
- **Log Format**: Structured JSON format for easy parsing

### Performance Tuning
- **Concurrent Workers**: Up to 10 devices for multi-device operations
- **Timeout Settings**: Configurable per tool
- **Memory Management**: Automatic cleanup of completed sessions
- **Error Recovery**: Retry logic for transient failures

---

## Error Handling

### Common Error Types
1. **Connection Errors**: GNS3 server unreachable
2. **Authentication Errors**: Invalid API credentials
3. **Device Errors**: Network device not responding
4. **Configuration Errors**: Invalid device configuration
5. **Timeout Errors**: Operations taking too long

### Error Recovery Strategies
1. **Automatic Retry**: For transient network issues
2. **Graceful Degradation**: Continue operation when possible
3. **Emergency Save**: Preserve progress during failures
4. **Detailed Logging**: Comprehensive error information for debugging

---

## Usage Examples

### Basic Usage
```python
from tools.gns3_topology_reader import GNS3TopologyTool

# Initialize tool
tool = GNS3TopologyTool()

# Get topology
topology = tool._run()

# Check for errors
if "error" in topology:
    print(f"Error: {topology['error']}")
else:
    print(f"Project: {topology['name']}")
    print(f"Nodes: {list(topology['nodes'].keys())}")
```

### Multi-Device Configuration
```python
from tools.config_tools_nornir import ExecuteMultipleDeviceConfigCommands

# Initialize tool
tool = ExecuteMultipleDeviceConfigCommands()

# Prepare configuration
device_configs = [
    {"device_name": "R-1", "config_commands": ["hostname Router-1"]},
    {"device_name": "R-2", "config_commands": ["hostname Router-2"]}
]

# Apply configuration
result = tool._run(device_configs)

# Check results
for device, outcome in result.items():
    if outcome["success"]:
        print(f"✓ {device}: Configuration applied successfully")
    else:
        print(f"✗ {device}: {outcome['error']}")
```

### Process Analyzer Integration
```python
from process_analyzer import LearningDocumentationCallback, LearningLangChainCallback

# Initialize callbacks
learning_cb = LearningDocumentationCallback(output_dir="reports")
langchain_cb = LearningLangChainCallback(learning_cb)

# Use with LangChain agent
agent.run("Configure OSPF", callbacks=[langchain_cb])

# Get session data
session_data = learning_cb.finalize_session()
generated_files = learning_cb.save_session_to_file(session_data)

print(f"Generated reports: {generated_files}")
```

---

*This API reference provides comprehensive documentation for all GNS3 Copilot components. For additional examples and usage patterns, see the main README.md and individual tool documentation.*
