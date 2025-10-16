# GNS3 Copilot - AI-Powered Network Automation Assistant

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.1.0+-green.svg)
![Chainlit](https://img.shields.io/badge/Chainlit-1.0.0+-purple.svg)
![GNS3](https://img.shields.io/badge/GNS3-2.2+-orange.svg)
![Nornir](https://img.shields.io/badge/Nornir-3.3.0+-red.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)

GNS3 Copilot is an intelligent network automation assistant that combines the power of AI with GNS3 network simulation platform. It uses DeepSeek LLM for natural language processing, LangChain for agent orchestration, and Chainlit for the web interface. It allows you to manage and configure network devices using natural language commands through a conversational interface with real-time reasoning display.

## 🚀 Features

- **Natural Language Interface**: Control network devices using simple English commands
- **Conversational AI**: Interactive chat-based interface powered by Chainlit with streaming responses
- **GNS3 Integration**: Seamlessly works with your existing GNS3 projects via REST API
- **Multi-Tool Support**: Execute display commands, configuration commands, and topology operations
- **Concurrent Multi-Device Operations**: Execute commands on multiple devices simultaneously using Nornir framework (up to 10 concurrent workers)
- **Real-time Reasoning**: Watch the AI agent's thought process in real-time using ReAct framework
- **Safety First**: Built-in safety mechanisms to prevent dangerous operations
- **Comprehensive Logging**: Detailed logs for debugging and auditing with separate log files for each tool
- **Dynamic Topology Discovery**: Automatically discovers devices and their console ports from GNS3 projects
- **Session Management**: Supports stop/cancel operations during long-running tasks

## 🔧 Technology Stack

- **AI Framework**: LangChain with ReAct (Reasoning + Acting) agent pattern
- **Language Model**: DeepSeek Chat LLM for natural language understanding and generation
- **Web Interface**: Chainlit for conversational UI with streaming responses
- **Network Automation**: Nornir framework for concurrent multi-device operations
- **Device Connectivity**: Netmiko for network device communication
- **Network Simulation**: GNS3 API integration for topology management
- **Logging**: Python logging with structured log files for each component

## 📋 Prerequisites

Before using GNS3 Copilot, ensure you have:

- **GNS3** installed and running (version 2.2 or later)
- **GNS3 Server** accessible at `http://localhost:3080`
- **Python 3.8+** installed
- **DeepSeek API Key** (optional, for enhanced AI capabilities)
- At least one **GNS3 project** with network devices (Preferably use Cisco IOSv devices; only tested with Cisco IOSv image.)

## 🛠 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yueguobin/gns3-copilot.git
cd gns3-copilot
```

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables** (optional):
Create a `.env` file in the project root:
```env
DEEPSEEK_API_KEY=your_api_key_here  # If using DeepSeek API
```

## 🎯 Quick Start

1. **Start GNS3 and open your project**
2. **Run the assistant**:
```bash
chainlit run gns3_copilot.py
```
or
```bash
chainlit run gns3_copilot.py --host 192.168.1.3 --port 8090
```

3. **Open your browser** to the URL shown in the terminal (typically `http://localhost:8000`)
4. **Start interacting** with natural language commands in the chat interface:
   - Enter commands in the chat input at the bottom
   - View real-time agent reasoning and execution steps
   - See final results displayed in the interface

## 💬 Example Commands

### Display Operations
- `"check R-1 and R-2 interfaces status"` (executes commands on multiple devices concurrently)
- `"show OSPF status on R-3 and R-4"` (executes commands on multiple devices concurrently)
- `"display running configuration on R-1"`

### Configuration Operations
- `"configure a loopback interface on R-3 with address 3.3.3.31/32"`
- `"enable OSPF on R-1"`
- `"set interface description on R-2 GigabitEthernet0/0"`

### Topology Operations
- `"show current topology"`
- `"list all devices in the project"`
- `"start all nodes"`

### Create Lab
- `"Create a topology with six routers. Test OSPF with multiple areas. Configure the hostname as the device name."`

## 🛡 Safety Features

GNS3 Copilot includes built-in safety mechanisms:

- **Command Validation**: Prevents execution of dangerous commands
- **Read-Only Mode**: Separate tools for display vs configuration operations
- **Error Handling**: Comprehensive error reporting and recovery
- **Logging**: All operations are logged for audit purposes

**Forbidden Commands**: The system will refuse to execute commands like `reload`, `write erase`, `erase startup-config`, and other destructive operations.

## 🏗 Architecture

```
GNS3 Copilot
├── Web Interface (Chainlit)
├── AI Agent (LangChain + DeepSeek)
├── Tool System
│   ├── GNS3TopologyTool - Reads project topology
│   ├── ExecuteMultipleDeviceCommands - Show commands on multiple devices (Nornir-based)
│   ├── ExecuteMultipleDeviceConfigCommands - Configuration commands on multiple devices (Nornir-based)
│   ├── ExecuteConfigCommands - Configuration commands (single device)
│   ├── GNS3TemplateTool - Get node templates
│   ├── GNS3CreateNodeTool - Node management
│   ├── GNS3LinkTool - Link management
│   └── GNS3StartNodeTool - Node control
└── GNS3 API Integration
```

## 📁 Project Structure

```
gns3-copilot/
├── gns3_copilot.py          # Main Chainlit application
├── requirements.txt         # Python dependencies
├── LICENSE                  # MIT License
├── .env                    # Environment variables (optional)
├── README.md               # This file
├── README_ZH.md            # Chinese documentation
├── chainlit.md             # Chainlit interface documentation
├── log/                    # Application logs
├── process_docs/           # Process analyzer documentation output
├── process_analyzer/       # Process analysis module
├── prompts/                # AI prompt templates
├── tools/                  # Tool implementations
└── docs/                   # Additional documentation
```

## 🐛 Troubleshooting

### Common Issues

1. **Connection refused to GNS3 server**
   - Ensure GNS3 server is running on `localhost:3080`
   - Check firewall settings

2. **Device not found in topology**
   - Verify device names match exactly
   - Ensure devices have console ports configured

3. **Command execution timeout**
   - Check device responsiveness
   - Increase timeout settings if needed

### Logs
Check the `log/` directory for detailed operation logs:
- `gns3_copilot.log` - Main application logs and session management
- `config_tools_nornir.log` - Multi-device configuration command executions (Nornir-based)
- `display_tools_nornir.log` - Multi-device display command executions (Nornir-based)
- `gns3_topology_reader.log` - GNS3 topology discovery and API interactions
- Other tool-specific log files

## 📚 Additional Documentation

- **[API Reference](docs/API_REFERENCE.md)** - Detailed API documentation for all tools and modules
- **[Contributing Guide](docs/CONTRIBUTING.md)** - Development contribution guidelines
- **[Process Analyzer](process_analyzer/README.md)** - Process analyzer module documentation
- **[README_ZH.md](README_ZH.md)** - Chinese documentation

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **GNS3 Team** for the excellent network simulation platform
- **LangChain** for the powerful AI agent framework
- **DeepSeek** for the AI language model capabilities
- **Chainlit** for the conversational UI framework
- **Netmiko** for network device communication
- **Nornir** for concurrent multi-device automation

---

**Version**: 1.0.0 - Stable release with full feature support
