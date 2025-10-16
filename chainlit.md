# GNS3 Copilot - AI-Powered Network Automation Assistant 🤖🌐

Welcome to **GNS3 Copilot** - your intelligent network automation companion! This AI-powered assistant combines DeepSeek LLM for natural language processing, LangChain for agent orchestration, and GNS3 network simulation to make network automation accessible and intuitive. It features real-time reasoning display using the ReAct framework.

## 🚀 What You Can Do

- **Natural Language Control**: Manage network devices using simple English commands
- **Real-time Reasoning**: Watch the AI agent's thought process in real-time using ReAct framework
- **Streaming Responses**: See the AI reasoning and results appear instantly in the chat
- **GNS3 Integration**: Seamlessly interact with your existing GNS3 projects via REST API
- **Multi-device Operations**: Execute commands across multiple devices simultaneously using Nornir (up to 10 concurrent workers)
- **Dynamic Topology Discovery**: Automatically discovers devices and their console ports from GNS3 projects
- **Session Management**: Supports stop/cancel operations during long-running tasks
- **Multi-device Configuration**: Configure multiple devices concurrently using Nornir framework
- **Safe Automation**: Built-in safety mechanisms prevent dangerous operations

## 🎯 Quick Start

1. **Start GNS3** and open your network project
2. **Enter commands** in the chat below to:
   - Check device status and configurations
   - Configure interfaces and protocols
   - Manage network topology
   - Troubleshoot connectivity issues

## 💬 Example Commands to Try

### Display Operations
- `"check R-1 and R-2 interfaces status"` (executes commands on multiple devices concurrently)
- `"show OSPF status on R-3 and R-4"` (executes commands on multiple devices concurrently)
- `"display running configuration on R-1"`

### Configuration Operations
- `"configure a loopback interface on R-3 with address 3.3.3.31/32"`
- `"enable OSPF on R-1"`
- `"set interface description on R-2 GigabitEthernet0/0"`
- `"configure loopback interfaces on R-1 and R-2 simultaneously"` (executes configuration on multiple devices concurrently)
- `"enable OSPF on all routers in the topology"` (executes configuration on multiple devices concurrently)

### Topology Operations
- `"show current topology"`
- `"list all devices in the project"`
- `"start all nodes"`

### Create Lab
- `"Create a topology with six routers. Test OSPF with multiple areas. Configure the hostname as the device name."`

## 🛡 Safety First

Your network is protected with:
- **Command Validation**: Prevents execution of dangerous commands
- **Read-Only Mode**: Separate tools for display vs configuration
- **Error Handling**: Comprehensive error reporting and recovery
- **Logging**: All operations are logged for audit purposes

**Forbidden Commands**: The system will refuse to execute commands like `reload`, `write erase`, `erase startup-config`, and other destructive operations.

## 🔧 Supported Devices

- **Primary Support**: Cisco IOSv (telnet console) - Currently tested and supported
- **Note**: Only Cisco IOSv devices have been tested and verified to work
- **Concurrent Operations**: Multi-device command execution using Nornir framework

## 📖 Need Help?

- **Documentation**: Check the project README.md for detailed setup instructions
- **Troubleshooting**: View logs in the `log/` directory for debugging:
  - `gns3_copilot.log` - Main application logs and session management
  - `config_tools_nornir.log` - Multi-device configuration executions
  - `display_tools_nornir.log` - Multi-device display command executions
  - `gns3_topology_reader.log` - GNS3 topology discovery and API interactions
  - Additional tool-specific logs for node/link management operations
- **Session Control**: Use the stop button to cancel long-running operations
- **Support**: Open issues on GitHub for assistance

## 📊 Process Analyzer Integration

The Chainlit interface seamlessly integrates with the Process Analyzer module to provide comprehensive session documentation:

### Automatic Report Generation
- **Real-time Capture**: Every command execution is automatically documented
- **Technical Reports**: Detailed analysis reports are shared directly in the chat after each execution
- **Session History**: Complete record of all interactions maintained in the `process_docs/` directory
- **Error Documentation**: Automatic capture and analysis of any errors or interruptions

### Report Features
- **Step-by-Step Documentation**: Complete ReAct execution cycles with timing information
- **Tool Usage Statistics**: Performance metrics and usage patterns
- **Error Recovery**: Documentation of interruption handling and recovery actions
- **Session Metadata**: Timestamps, user input, and execution duration

### Accessing Reports
- **In Chat**: Technical reports automatically appear as downloadable files after each command
- **File System**: All reports are saved to `process_docs/` with timestamp-based naming
- **Historical Analysis**: Complete session history available for review and learning

## 🎉 Ready to Automate?

Start by typing a network command in the chat below! The AI assistant will guide you through the process and show you exactly what it's doing every step of the way.

## 🔧 Technology Stack

- **AI Framework**: LangChain with ReAct (Reasoning + Acting) agent pattern
- **Language Model**: DeepSeek Chat LLM for natural language understanding
- **Web Interface**: Chainlit for conversational UI with streaming responses
- **Network Automation**: Nornir framework for concurrent multi-device operations
- **Device Connectivity**: Netmiko for network device communication
- **Network Simulation**: GNS3 API integration for topology management
- **Process Analysis**: Comprehensive session documentation and error handling

---

*Powered by Chainlit, LangChain, DeepSeek, GNS3 API, Nornir, and Process Analyzer*
