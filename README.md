# GNS3 Copilot

An AI-powered network automation assistant designed for GNS3 network simulator, providing intelligent network device management and automated operations.

## Project Introduction

GNS3 Copilot is a powerful network automation tool that integrates multiple AI models and network automation frameworks, enabling natural language interaction with users to perform network device configuration, topology management, and fault diagnosis tasks.

### Core Features

- 🤖 **AI-driven Conversational Interface**: Supports natural language interaction to understand network automation requirements
- 🔧 **Device Configuration Management**: Batch configuration of network devices, supporting multiple vendor devices(Currently only Cisco IOSv images have been tested)
- 📊 **Topology Management**: Automatically create, modify, and manage GNS3 network topologies
- 🔍 **Network Diagnostics**: Intelligent network troubleshooting and performance monitoring
- 🌐 **Multi-LLM Support**: Integrates DeepSeek, Google Gemini, and other AI models

## Technical Architecture

### Core Components

- **Agent Framework**: Intelligent agent system built on LangChain v1.0.2 and LangGraph
- **Network Automation**: Network device automation using Nornir v3.5.0 and Netmiko v4.6.0
- **GNS3 Integration**: Custom GNS3 API client supporting topology and node management
- **AI Models**: Support for large language models like DeepSeek Cha

### Tool Set

| Tool Name | Function Description |
|-----------|---------------------|
| `GNS3TopologyTool` | Read GNS3 topology information |
| `GNS3CreateNodeTool` | Create GNS3 nodes |
| `GNS3LinkTool` | Create connections between nodes |
| `GNS3StartNodeTool` | Start GNS3 nodes |
| `GNS3TemplateTool` | Get node templates |
| `ExecuteMultipleDeviceCommands` | Execute show commands |
| `ExecuteMultipleDeviceConfigCommands` | Execute configuration commands |

## Installation Guide

### System Requirements

- Python 3.8+
- GNS3 Server (running on http://localhost:3080)
- Supported Operating Systems: Windows, macOS, Linux

### Installation Steps

1. **Clone the project**
```bash
git clone https://github.com/yueguobin/gns3-copilot.git
cd gns3-copilot
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create `.env` file and configure API keys:
```env
DEEPSEEK_API_KEY="your_deepseek_api_key"
```

5. **Start GNS3 Server**
Ensure GNS3 Server is running at the default address `http://localhost:3080`

## Usage Guide

### Launch Methods

#### Method 1: Direct Python Code Execution

```python
from agent.gns3_copilot import agent

# Use AI agent for network automation
response = agent.invoke("Check the interface status of all routers")
print(response)
```

#### Method 2: LangGraph Development Server

```bash
# Start LangGraph development server
langgraph dev

# Server will start at http://localhost:2024
# Interact with the agent via web interface or API
```

#### Method 3: LangGraph Tunnel Mode (Remote Access)

```bash
# Start development server with tunnel functionality
langgraph dev --tunnel

# Generate public access URL for remote access
# Suitable for scenarios requiring external network access to the agent
```

**LangGraph Server Notes:**
- Default port: 2024
- Configuration file: `langgraph.json`
- Graph ID: `agent`
- Supports hot reload and real-time debugging
- Provides Swagger API documentation

### Basic Usage

### Feature Examples

#### 1. Topology Management
```python
# Get current topology information
topology = agent.invoke("Show current network topology")

# Create new node
agent.invoke("Create a router node named R3")

# Connect devices
agent.invoke("Connect R3's Gi0/0 interface to R1's Gi0/1 interface")
```

#### 2. Device Configuration
```python
# Batch configure interfaces
agent.invoke("""
Configure loopback interfaces for all routers:
- R1: Loopback0 IP 1.1.1.1/32
- R2: Loopback0 IP 2.2.2.2/32
""")

# Configure routing protocols
agent.invoke("Enable OSPF process 1 on all routers and advertise all interfaces")
```

#### 3. Network Diagnostics
```python
# Check device status
agent.invoke("Check the running status and CPU usage of all devices")

# Network connectivity testing
agent.invoke("Test network connectivity from R1 to R2")

# Routing table check
agent.invoke("Show routing tables of all routers")
```

### Supported Command Types

#### Show Commands (Read-only)
- `show version`
- `show ip interface brief`
- `show running-config`
- `show ip route`
- `show ospf neighbor`
- `show interfaces status`

#### Configuration Commands (Use with caution)
- `interface <interface>`
- `ip address <ip> <mask>`
- `router ospf <process>`
- `network <network> area <area>`
- `description <text>`

## Project Structure

```
gns3-copilot/
├── agent/                    # Core agent modules
│   └── gns3_copilot.py      # Main agent implementation
├── tools_v2/                 # Tool set (v2)
│   ├── __init__.py
│   ├── config_tools_nornir.py      # Configuration tools
│   ├── display_tools_nornir.py     # Display tools
│   ├── gns3_topology_reader.py     # Topology reader
│   ├── gns3_create_node.py         # Node creation
│   ├── gns3_create_link.py         # Link creation
│   ├── gns3_start_node.py          # Node startup
│   ├── gns3_get_node_temp.py       # Template retrieval
│   ├── custom_gns3fy.py           # Custom GNS3 client
│   └── logging_config.py          # Logging configuration
├── prompts/                  # Prompts
│   ├── __init__.py
│   └── react_prompt.py       # System prompts
├── test/                     # Test files
├── log/                      # Log directory
├── requirements.txt          # Dependencies list
├── langgraph.json           # LangGraph configuration
├── .env                     # Environment variables
└── README.md               # Project documentation
```

## Dependencies

### Core Dependencies

- **AI Framework**: 
  - `langchain>=1.0.2` - Core LangChain framework
  - `langchain-core>=1.0.1` - LangChain core components
  - `langchain-deepseek>=1.0.0` - DeepSeek integration
  - `langchain-google-genai>=3.0.0` - Google Gemini integration
  - `langgraph>=1.0.0` - LangGraph for agent workflows
  - `langgraph-cli>=0.4.4` - LangGraph CLI tool

- **Network Automation**:
  - `netmiko>=4.6.0` - Network device automation
  - `nornir>=3.5.0` - Network automation framework
  - `nornir-netmiko>=1.0.1` - Nornir-Netmiko integration
  - `nornir-utils>=0.2.0` - Nornir utilities
  - `nornir_salt>=0.22.5` - Nornir Salt integration

- **HTTP & Authentication**:
  - `requests>=2.32.5` - HTTP requests
  - `urllib3>=2.5.0` - HTTP library with SSL support
  - `PyJWT>=2.10.1` - JWT authentication for GNS3 API v3

- **Data & Environment**:
  - `pydantic>=2.12.3` - Data validation
  - `python-dotenv>=1.2.1` - Environment variable management

## Configuration Guide

### GNS3 Server Configuration

Ensure GNS3 Server is properly configured:
- Default port: 3080
- Enable HTTP API
- Configure appropriate emulator images

### Logging Configuration

The project uses a unified logging system, with log files saved in the `log/` directory:
- `gns3_copilot.log`: Main application log
- `display_tools_nornir.log`: Display tools log
- `config_tools_nornir.log`: Configuration tools log

### AI Model Configuration

Supports multiple AI models, switch in `agent/gns3_copilot.py`:

```python
# Use DeepSeek (default)
llm = ChatDeepSeek(model="deepseek-chat", temperature=0, streaming=True)
```

## Security Considerations

⚠️ **Important Security Notes**:

1. **Configuration Command Security**: Configuration tools can modify device configurations. Before use, ensure:
   - Verify in test environment
   - Backup important configurations
   - Understand the purpose of each command

2. **API Key Protection**: 
   - Do not commit `.env` file to version control
   - Rotate API keys regularly
   - Follow principle of least privilege

3. **Network Isolation**: Recommended to use in isolated test environment

## Troubleshooting

### Common Issues

1. **GNS3 Connection Failure**
   - Check if GNS3 Server is running
   - Confirm port 3080 is accessible
   - Check firewall settings
   - Verify API version compatibility

2. **Device Connection Issues**
   - Confirm device console ports are correct
   - Check if devices are started
   - Verify Telnet connection

3. **AI Model Call Failure**
   - Check if API keys are correct
   - Confirm network connection
   - Verify API quota

4. **Authentication Issues**
   - For GNS3 v3, ensure JWT token is properly configured(test)
   - Check API credentials in environment variables

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing Guide

Contributions are welcome! Please follow these steps:

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- Project Homepage: https://github.com/yueguobin/gns3-copilot
- Issue Tracker: https://github.com/yueguobin/gns3-copilot/issues

## Changelog

### Version 1.0.2 (October 27, 2025)
- Updated all dependencies to latest stable versions
- Added PyJWT and urllib3 for GNS3 v3 API support(test)
- Added langgraph-cli for LangGraph server functionality
- Updated project structure to use tools_v2 directory
- Enhanced authentication support for both GNS3 v2 and v3(test)

### Version 1.0.0 (October 20, 2025)
- Updated to use langchain 1.0.0 version
- Removed custom callback functions and report generation features
- Removed chainlit UI interface
- Using langgraph studio

---

**Disclaimer**: This tool is intended for educational and testing purposes only. Before using in production environments, please test thoroughly and ensure compliance with your security policies.
