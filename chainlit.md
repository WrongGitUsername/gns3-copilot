# GNS3 Copilot - AI-Powered Network Automation Assistant 🤖🌐

Welcome to **GNS3 Copilot** - your intelligent network automation companion! This AI-powered assistant combines the power of natural language processing with GNS3 network simulation to make network automation accessible and intuitive.

## 🚀 What You Can Do

- **Natural Language Control**: Manage network devices using simple English commands
- **Real-time Reasoning**: Watch the AI agent's thought process as it works
- **GNS3 Integration**: Seamlessly interact with your existing GNS3 projects
- **Multi-device Operations**: Execute commands across multiple devices simultaneously using Nornir
- **Concurrent Execution**: Run commands on multiple devices at the same time for faster results
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

- **Primary Support**: Cisco IOSv (telnet console)
- **Extensible**: Other network devices via Netmiko
- **Concurrent Operations**: Multi-device command execution using Nornir framework

## 📖 Need Help?

- **Documentation**: Check the project README.md for detailed setup instructions
- **Troubleshooting**: View logs in the `log/` directory for debugging
- **Support**: Open issues on GitHub for assistance

## 🎉 Ready to Automate?

Start by typing a network command in the chat below! The AI assistant will guide you through the process and show you exactly what it's doing every step of the way.

---

*Powered by Chainlit, LangChain, DeepSeek, GNS3 API, and Nornir*
