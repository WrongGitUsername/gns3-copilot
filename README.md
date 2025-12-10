# GNS3 Copilot

![Python](https://img.shields.io/badge/python-3.8+-blue.svg) ![GNS3](https://img.shields.io/badge/GNS3-2.2+-green.svg) ![LangChain](https://img.shields.io/badge/LangChain-1.0.7-orange.svg) ![Nornir](https://img.shields.io/badge/Nornir-3.5.0-red.svg) ![Netmiko](https://img.shields.io/badge/Netmiko-4.6.0-blue.svg) ![LangGraph](https://img.shields.io/badge/LangGraph-1.0.0-purple.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg) ![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

An AI-powered network automation assistant designed specifically for GNS3 network simulator, providing intelligent network device management and automated operations.

## Project Overview

GNS3 Copilot is a powerful network automation tool that integrates multiple AI models and network automation frameworks. It can interact with users through natural language and perform tasks such as network device configuration, topology management, and fault diagnosis.

<img src="https://raw.githubusercontent.com/yueguobin/gns3-copilot/refs/heads/master/demo.gif" alt="GNS3 Copilot Function demonstration" width="1280"/>

### Core Features

- 🤖 **AI-Powered Chat Interface**: Supports natural language interaction, understands network automation requirements
- 🔧 **Device Configuration Management**: Batch configuration of network devices, supports multiple vendor devices (currently tested with Cisco IOSv image only)
- 📊 **Topology Management**: Automatically create, modify, and manage GNS3 network topologies
- 🔍 **Network Diagnostics**: Intelligent network troubleshooting and performance monitoring
- 🌐 **LLM Support**: Integrated DeepSeek AI model for natural language processing



## Technical Architecture

### Core Components

- **Agent Framework**: Intelligent agent system built on LangChain v1.0.7 and LangGraph
- **Network Automation**: Network device automation using Nornir v3.5.0 and Netmiko v4.6.0
- **GNS3 Integration**: Custom GNS3 API client supporting topology and node management with JWT authentication capability
- **AI Models**: Supports DeepSeek Chat large language model

### Toolset

| Tool Name | Function Description |
|-----------|---------------------|
| `GNS3TopologyTool` | Read GNS3 topology information |
| `GNS3CreateNodeTool` | Create GNS3 nodes |
| `GNS3LinkTool` | Create connections between nodes |
| `GNS3StartNodeTool` | Start GNS3 nodes |
| `GNS3TemplateTool` | Get node templates |
| `ExecuteMultipleDeviceCommands` | Execute display commands |
| `ExecuteMultipleDeviceConfigCommands` | Execute configuration commands |
| `VPCSMultiCommands` | Execute VPCS commands on multiple devices |
| `LinuxTelnetBatchTool` | Execute linux commands on multiple devices |

## Installation Guide

### Environment Requirements

- Python 3.8+
- GNS3 Server (running on http://localhost:3080 or remote host)
- Supported operating systems: Windows, macOS, Linux

### Installation Steps

1. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

1. **Install GNS3 Copilot**
```bash
pip install gns3-copilot
```

1. **Start GNS3 Server**
Ensure GNS3 Server is running and can be accessed via its API interface: `http://x.x.x.x:3080`

1. **Launch the application**
```bash
gns3-copilot
```

## Usage Guide

### Startup

```bash
# Basic startup
gns3-copilot

# Specify custom port
gns3-copilot --server.port 8080

# Specify address and port
gns3-copilot --server.address 0.0.0.0 --server.port 8080

# Run in headless mode
gns3-copilot --server.headless true

# Set log level
gns3-copilot --logger.level debug

# Disable usage statistics
gns3-copilot --browser.gatherUsageStats false

# Get help
gns3-copilot --help

# Show version
gns3-copilot --version
```


### Configure on Settings Page

**Configure using First-Party Providers**

![First-Party Providers](https://github.com/yueguobin/gns3-copilot/blob/master/Config_First-Party.jpeg?raw=true)

**Configure using Third-Party Aggregators**

![Third-Party Aggregators](https://github.com/yueguobin/gns3-copilot/blob/master/Config_Third-Party-Aggregator.jpeg?raw=true)

### Configuration Parameters Details

#### 📋 Configuration File Overview

GNS3 Copilot configuration is managed through a Streamlit interface, with all settings saved in the `.env` file in the project root directory. If the `.env` file doesn't exist on first run, the system will automatically create it.

#### 🔧 Main Configuration Content

##### 1. GNS3 Server Configuration
- **GNS3 Server Host**: GNS3 server host address (e.g., 127.0.0.1)
- **GNS3 Server URL**: Complete GNS3 server URL (e.g., http://127.0.0.1:3080)
- **API Version**: GNS3 API version (supports v2 and v3)
- **GNS3 Server Username**: GNS3 server username (required only for API v3)
- **GNS3 Server Password**: GNS3 server password (required only for API v3)

##### 2. LLM Model Configuration
- **Model Provider**: Model provider (supports: openai, anthropic, deepseek, xai, openrouter, etc.)
- **Model Name**: Specific model name (e.g., deepseek-chat, gpt-4o-mini, etc.)
- **Model API Key**: Model API key
- **Base URL**: Base URL for model service (required when using third-party platforms like OpenRouter)
- **Temperature**: Model temperature parameter (controls output randomness, range 0.0-1.0)

##### 3. Other Settings
- **Linux Console Username**: Linux console username (for Debian devices in GNS3)
- **Linux Console Password**: Linux console password

#### ⚠️ Important Notes

##### 1. Configuration File Management
- Configuration is automatically saved in the `.env` file in the project root directory
- If the `.env` file doesn't exist, the system will automatically create it
- A warning will be displayed on first run indicating the configuration file has been created

##### 2. GNS3 Server API Version Compatibility
- **API v2**: No username and password authentication required
- **API v3**: Username and password authentication required
- The system dynamically shows/hides authentication fields based on the selected API version

##### 3. Model Configuration Key Points
- **OpenRouter Platform Usage**:
  - Model Provider should be filled as "openai"
  - Base URL must be filled: `https://openrouter.ai/api/v1`
  - Model Name format: `openai/gpt-4o-mini` or `x-ai/grok-4-fast`

##### 4. Security Considerations
- API Key field uses password type input, content will be hidden
- Recommend regular API key rotation
- Do not commit `.env` file to version control system

##### 5. Configuration Validation
- The system performs basic validation on configuration items:
  - API version can only be "2" or "3"
  - Model Provider must be in the supported list
  - Temperature must be a valid number format

##### 6. Linux Device Configuration
- Username and password are used to connect to Debian Linux devices in GNS3
- Default example username and password are both "debian"
- Ensure Debian devices are properly configured in GNS3

#### 🚀 Usage Recommendations

1. **First-time Configuration**: Fill in each item according to the interface prompts, items with `*` are required
2. **Test Connection**: After configuration, it's recommended to test GNS3 server connection first
3. **Model Selection**: Choose appropriate model provider and specific model based on your needs
4. **Backup Configuration**: Regularly backup `.env` file to prevent configuration loss


## Security Considerations

1. **API Key Protection**:
   - Do not commit `.env` file to version control
   - Regularly rotate API keys
   - Use principle of least privilege


## Troubleshooting

### Common Issues

1. **GNS3 Connection Failure**
   - Check if GNS3 Server is running
   - Confirm port 3080 is accessible
   - Check firewall settings

2. **Device Connection Issues**
   - Confirm device console ports are correct
   - Check if devices are started
   - Verify Telnet connections

3. **AI Model Call Failures**
   - Check if API keys are correct
   - Confirm network connectivity
   - Verify API quotas

4. **Authentication Issues**
   - For GNS3 v3, ensure JWT tokens are properly configured (under testing)
   - Check API credentials in environment variables


## Contribution Guidelines

Welcome to contribute code! Please follow these steps:

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

This project uses MIT License - see [LICENSE](LICENSE) file for details.

## Contact

- Project Homepage: https://github.com/yueguobin/gns3-copilot
- Issue Reporting: https://github.com/yueguobin/gns3-copilot/issues

---

**Disclaimer**: This tool is for educational and testing purposes only. Before using in production environment, please thoroughly test and ensure it complies with your security policies.
