# GNS3 Copilot API Reference

This document provides detailed API documentation for all tools and modules in the GNS3 Copilot project.

## Table of Contents

- [Core Tools](#core-tools)
- [Process Analyzer](#process-analyzer)
- [Utility Modules](#utility-modules)
- [Configuration](#configuration)

## Core Tools

### GNS3TopologyTool

**Location**: `tools/gns3_topology_reader.py`

Retrieves the topology of the currently open GNS3 project.

#### Methods

##### `_run(tool_input=None, run_manager=None) -> dict`

**Description**: Synchronous method to retrieve the topology of the currently open GNS3 project.

**Parameters**:
- `tool_input` (optional): Input parameters, typically a dict or Pydantic model containing server_url
- `run_manager` (optional): Callback manager for tool run

**Returns**:
- `dict`: A dictionary containing:
  - `project_id` (str): UUID of the open project
  - `name` (str): Project name
  - `status` (str): Project status (e.g., 'opened')
  - `nodes` (dict): Dictionary with node names as keys and details as values
  - `links` (list): List of link details
  - `error` (str): Error message if an exception occurs

**Example Output**:
```json
{
    "project_id": "f32ebf3d-ef8c-4910-b0d6-566ed828cd24",
    "name": "network llm iosv",
    "status": "opened",
    "nodes": {
        "R-1": {
            "node_id": "e5ca32a8-9f5d-45b0-82aa-ccfbf1d1a070",
            "name": "R-1",
            "ports": [
                {"name": "Gi0/0", "adapter_number": 0, "port_number": 0, "link_type": "ethernet"}
            ],
            "console_port": 5000,
            "type": "qemu"
        }
    },
    "links": [("R-1", "Gi0/0", "R-2", "Gi0/0")]
}
```

**Error Handling**:
- Returns empty dict if no projects found or no project is open
- Returns error dict if exception occurs during retrieval

---

### ExecuteMultipleDeviceCommands

**Location**: `tools/display_tools_nornir.py`

Executes show/display commands on multiple devices concurrently using Nornir framework.

#### Methods

##### `_run(device_names, commands, run_manager=None) -> dict`

**Description**: Executes display commands on multiple network devices simultaneously.

**Parameters**:
- `device_names` (list): List of device names to execute commands on
- `commands` (list): List of show/display commands to execute
- `run_manager` (optional): Callback manager for tool run

**Returns**:
- `dict`: Results organized by device name with command outputs and execution status

**Example Usage**:
```python
tool = ExecuteMultipleDeviceCommands()
result = tool._run(
    device_names=["R-1", "R-2"],
    commands=["show ip interface brief", "show version"]
)
```

**Features**:
- Concurrent execution on up to 10 devices
- Automatic device discovery from GNS3 topology
- Comprehensive error handling per device
- Detailed logging of execution process

**Device Compatibility**:
- **Cisco IOSv** (primary support, telnet console) - Currently tested and supported
- **Note**: Only Cisco IOSv devices have been tested and verified to work

---

### ExecuteMultipleDeviceConfigCommands

**Location**: `tools/config_tools_nornir.py`

Executes configuration commands on multiple devices concurrently using Nornir framework.

#### Methods

##### `_run(device_configs, run_manager=None) -> dict`

**Description**: Applies configuration commands to multiple network devices simultaneously.

**Parameters**:
- `device_configs` (list): List of dictionaries containing device names and config commands
- `run_manager` (optional): Callback manager for tool run

**Example Input**:
```python
[
    {"device_name": "R-1", "config_commands": ["router ospf 1", "network 10.0.0.0 0.0.0.255 area 0"]},
    {"device_name": "R-2", "config_commands": ["router ospf 1", "network 20.0.0.0 0.0.0.255 area 0"]}
]
```

**Returns**:
- `dict`: Configuration results organized by device with success/failure status

**Safety Features**:
- Command validation to prevent dangerous operations
- Rollback capability on configuration failures
- Comprehensive logging of all configuration changes

---

### GNS3CreateNodeTool

**Location**: `tools/gns3_create_node.py`

Creates new nodes in GNS3 projects.

#### Methods

##### `_run(node_name, node_template, run_manager=None) -> dict`

**Description**: Creates a new node in the current GNS3 project.

**Parameters**:
- `node_name` (str): Name for the new node
- `node_template` (str): Template name for the node type
- `run_manager` (optional): Callback manager for tool run

**Returns**:
- `dict`: Node creation result with node ID and status

---

### GNS3LinkTool

**Location**: `tools/gns3_create_link.py`

Creates links between nodes in GNS3 projects.

#### Methods

##### `_run(node1, port1, node2, port2, run_manager=None) -> dict`

**Description**: Creates a network link between two nodes.

**Parameters**:
- `node1` (str): First node name
- `port1` (str): Port name on first node
- `node2` (str): Second node name
- `port2` (str): Port name on second node
- `run_manager` (optional): Callback manager for tool run

**Returns**:
- `dict`: Link creation result with link ID and status

---

### GNS3StartNodeTool

**Location**: `tools/gns3_start_node.py`

Controls the power state of GNS3 nodes.

#### Methods

##### `_run(node_name, action, run_manager=None) -> dict`

**Description**: Starts, stops, or restarts a GNS3 node.

**Parameters**:
- `node_name` (str): Name of the node to control
- `action` (str): Action to perform ("start", "stop", "restart")
- `run_manager` (optional): Callback manager for tool run

**Returns**:
- `dict`: Node control result with status information

---

### GNS3TemplateTool

**Location**: `tools/gns3_get_node_temp.py`

Retrieves available node templates from GNS3 server.

#### Methods

##### `_run(tool_input=None, run_manager=None) -> dict`

**Description**: Gets list of available node templates for creating new nodes.

**Parameters**:
- `tool_input` (optional): Input parameters (not used)
- `run_manager` (optional): Callback manager for tool run

**Returns**:
- `dict`: Available templates with details about each template type

---

## Process Analyzer

### LearningDocumentationCallback

**Location**: `process_analyzer/process_callback.py`

Core callback handler for capturing and documenting execution processes.

#### Methods

##### `start_new_session(user_input) -> str`

**Description**: Starts a new documentation session.

**Parameters**:
- `user_input` (str): The user's input/command

**Returns**:
- `str`: Session ID for tracking

##### `record_complete_step(thought, tool_name, action_input) -> None`

**Description**: Records a complete ReAct execution step.

**Parameters**:
- `thought` (str): The agent's thought process
- `tool_name` (str): Name of the tool being used
- `action_input` (list): Input parameters for the tool

##### `add_observation_to_current_step(observation) -> None`

**Description**: Adds the observation/result to the current step.

**Parameters**:
- `observation` (str): The tool's output/result

##### `record_final_answer(answer) -> None`

**Description**: Records the final answer of the execution.

**Parameters**:
- `answer` (str): The final result/conclusion

##### `finalize_session() -> dict`

**Description**: Finalizes the session and returns complete session data.

**Returns**:
- `dict`: Complete session data including all steps and metadata

##### `emergency_save(reason) -> None`

**Description**: Performs emergency save during interruption.

**Parameters**:
- `reason` (str): Reason for the emergency save

---

### LearningLangChainCallback

**Location**: `process_analyzer/langchain_callback.py`

LangChain callback handler for automatic process capture.

#### Methods

##### `on_agent_action(action, **kwargs) -> None`

**Description**: Called when agent performs an action.

**Parameters**:
- `action`: The action being performed
- `**kwargs`: Additional keyword arguments

##### `on_tool_end(output, **kwargs) -> None`

**Description**: Called when a tool finishes execution.

**Parameters**:
- `output`: The tool's output
- `**kwargs`: Additional keyword arguments

##### `on_agent_finish(finish, **kwargs) -> None`

**Description**: Called when agent finishes execution.

**Parameters**:
- `finish`: The final result
- `**kwargs`: Additional keyword arguments

##### `on_agent_error(error, **kwargs) -> None`

**Description**: Called when an error occurs during agent execution.

**Parameters**:
- `error`: The error that occurred
- `**kwargs`: Additional keyword arguments

---

## Utility Modules

### Logging Configuration

**Location**: `tools/logging_config.py`

Provides centralized logging configuration for all tools.

#### Functions

##### `setup_tool_logger(tool_name, log_file=None) -> logging.Logger`

**Description**: Sets up a configured logger for a specific tool.

**Parameters**:
- `tool_name` (str): Name of the tool
- `log_file` (str, optional): Custom log file path

**Returns**:
- `logging.Logger`: Configured logger instance

**Features**:
- Automatic log file creation in `log/` directory
- Structured logging with timestamps
- Different log levels for development and production
- Log rotation to prevent disk space issues

---

### Custom GNS3fy

**Location**: `tools/custom_gns3fy.py`

Custom GNS3 API adapter with enhanced functionality.

#### Classes

##### `Gns3Connector`

Enhanced GNS3 server connector with error handling and retry logic.

##### `Project`

GNS3 project management with additional utility methods.

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

### Error Response Format

```json
{
    "error": "Error description",
    "error_type": "ConnectionError",
    "timestamp": "2025-01-01T12:00:00Z",
    "context": "Additional context information"
}
```

---

## Examples

### Basic Usage Example

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

### Multi-Device Configuration Example

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

### Process Analyzer Integration Example

```python
from process_analyzer import LearningDocumentationCallback, LearningLangChainCallback

# Initialize callbacks
learning_cb = LearningDocumentationCallback(output_dir="process_docs")
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
