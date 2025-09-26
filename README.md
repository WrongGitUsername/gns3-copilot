# GNS3 Copilot - AI-Powered Network Automation Assistant

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.1.0+-green.svg)
![GNS3](https://img.shields.io/badge/GNS3-2.2+-orange.svg)

GNS3 Copilot is an intelligent network automation assistant that combines the power of AI with GNS3 network simulation platform. It allows you to manage and configure network devices using natural language commands.

## 🚀 Features

- **Natural Language Interface**: Control network devices using simple English commands
- **GNS3 Integration**: Seamlessly works with your existing GNS3 projects
- **Multi-Tool Support**: Execute display commands, configuration commands, and topology operations
- **Safety First**: Built-in safety mechanisms to prevent dangerous operations
- **Real-time Interaction**: Live communication with network devices
- **Comprehensive Logging**: Detailed logs for debugging and auditing

## 📋 Prerequisites

Before using GNS3 Copilot, ensure you have:

- **GNS3** installed and running (version 2.2 or later)
- **GNS3 Server** accessible at `http://localhost:3080`
- **Python 3.8+** installed
- At least one **GNS3 project** with network devices (preferably Cisco IOS devices)

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
python gns3_copilot.py
```

3. **Start interacting** with natural language commands:
```
GNS3 Network Assistant - input 'quit' to exit

Please enter your question: check R-1 and R-2 interfaces status
```

## 💬 Example Commands

### Display Operations
- `"check R-1 and R-2 interfaces status"`
- `"show OSPF status on R-3 and R-4"`
- `"display running configuration on R-1"`

### Configuration Operations
- `"configure a loopback interface on R-3 with address 3.3.3.31/32"`
- `"enable OSPF on R-1"`
- `"set interface description on R-2 GigabitEthernet0/0"`

### Topology Operations
- `"show current topology"`
- `"list all devices in the project"`
- `"start all nodes"`

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
├── AI Agent (LangChain + DeepSeek)
├── Tool System
│   ├── GNS3TopologyTool - Reads project topology
│   ├── ExecuteDisplayCommands - Show commands
│   ├── ExecuteConfigCommands - Configuration commands
│   ├── GNS3CreateNodeTool - Node management
│   ├── GNS3LinkTool - Link management
│   └── GNS3StartNodeTool - Node control
└── GNS3 API Integration
```

## 🔧 Available Tools

### Core Tools
- **GNS3 Topology Reader**: Retrieves current project topology
- **Display Commands Executor**: Executes show commands on devices
- **Configuration Commands Executor**: Applies configuration changes
- **Node Management**: Create, start, and manage GNS3 nodes
- **Link Management**: Create and manage network links

### Supported Device Types
- Cisco IOS (primary support, telnet console)
- Other network devices via Netmiko (extensible)

## 📁 Project Structure

```
gns3-copilot/
├── gns3_copilot.py          # Main application
├── requirements.txt         # Python dependencies
├── LICENSE                  # MIT License
├── .env                    # Environment variables (optional)
├── README.md               # This file
├── log/                    # Application logs
└── tools/                  # Tool implementations
    ├── config_tools.py     # Configuration commands
    ├── display_tools.py    # Display commands
    ├── gns3_topology_reader.py
    ├── gns3_create_node.py
    ├── gns3_create_link.py
    ├── gns3_start_node.py
    ├── gns3_get_node_temp.py
    └── custom_gns3fy.py    # GNS3 API adapter
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
- `display_tools.log` - Display command executions
- `device_config_tool.log` - Configuration operations
- `gns3_topology_reader.log` - Topology reading operations

## 🤝 Contributing

We welcome contributions! Please feel free to submit pull requests or open issues for:

- New device support
- Additional tools and features
- Bug fixes and improvements
- Documentation enhancements

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **GNS3 Team** for the excellent network simulation platform
- **LangChain** for the powerful AI agent framework
- **DeepSeek** for the AI language model capabilities
- **Netmiko** for network device communication

## 📞 Support

For questions and support:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review the code documentation

---

**Note**: This is an alpha version. Features and APIs may change as the project evolves.
