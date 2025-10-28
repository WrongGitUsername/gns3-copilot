# GNS3 Copilot

An AI-powered network automation assistant designed for GNS3 network simulator, providing intelligent network device management and automated operations.

## Project Introduction

GNS3 Copilot is a powerful network automation tool that integrates multiple AI models and network automation frameworks, enabling natural language interaction with users to perform network device configuration, topology management, and fault diagnosis tasks.

### Core Features

- 🤖 **AI-driven Conversational Interface**: Supports natural language interaction to understand network automation requirements
- 🔧 **Device Configuration Management**: Batch configuration of network devices, supporting multiple vendor devices (Currently only Cisco IOSv images have been tested)
- 📊 **Topology Management**: Automatically create, modify, and manage GNS3 network topologies
- 🔍 **Network Diagnostics**: Intelligent network troubleshooting and performance monitoring
- 🌐 **LLM Support**: Integrates DeepSeek AI models for natural language processing

## Technical Architecture

### Core Components

- **Agent Framework**: Intelligent agent system built on LangChain v1.0.2 and LangGraph
- **Network Automation**: Network device automation using Nornir v3.5.0 and Netmiko v4.6.0
- **GNS3 Integration**: Custom GNS3 API client supporting topology and node management
- **AI Models**: Support for DeepSeek Chat large language model

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
Copy the environment template and configure your settings:
```bash
cp env.example .env
```

Edit the `.env` file with your configuration:
```env
# API Keys for LLM providers
DEEPSEEK_API_KEY="your_deepseek_api_key_here"

# GNS3 Server Configuration
GNS3_SERVER_HOST="127.0.0.1"
GNS3_SERVER_URL="http://127.0.0.1:3080"
GNS3_SERVER_USERNAME=""
GNS3_SERVER_PASSWORD=""

# API Version
API_VERSION="2"
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


---

**Disclaimer**: This tool is intended for educational and testing purposes only. Before using in production environments, please test thoroughly and ensure compliance with your security policies.
