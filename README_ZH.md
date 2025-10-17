# GNS3 Copilot - AI网络自动化助手

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.1.0+-green.svg)
![Chainlit](https://img.shields.io/badge/Chainlit-1.0.0+-purple.svg)
![GNS3](https://img.shields.io/badge/GNS3-2.2+-orange.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)

GNS3 Copilot 是一个智能网络自动化助手，结合AI与GNS3网络仿真平台。使用DeepSeek LLM进行自然语言处理，LangChain进行智能体编排，Chainlit提供Web界面，通过对话界面和实时推理显示，使用自然语言命令管理和配置网络设备。

## 🚀 核心功能

- **自然语言界面**：使用简单英语命令控制网络设备
- **对话式AI**：基于Chainlit的交互式聊天界面，支持流式响应
- **GNS3集成**：通过REST API无缝连接现有GNS3项目
- **多工具支持**：执行显示命令、配置命令和拓扑操作
- **并发多设备操作**：使用Nornir框架同时执行多设备命令（最多10个并发工作线程）
- **实时推理**：使用ReAct框架实时观看AI智能体思考过程
- **安全机制**：内置安全机制防止危险操作
- **完整日志**：详细日志记录，每个工具独立日志文件
- **动态拓扑发现**：自动发现GNS3项目中的设备和控制台端口
- **会话管理**：支持长时间运行任务的停止/取消操作

## 🔧 技术栈

- **AI框架**：LangChain + ReAct智能体模式
- **语言模型**：DeepSeek Chat LLM
- **Web界面**：Chainlit对话式UI
- **网络自动化**：Nornir框架并发多设备操作
- **设备连接**：Netmiko网络设备通信
- **网络仿真**：GNS3 API集成拓扑管理
- **日志记录**：Python结构化日志

## 📋 环境要求

- **GNS3** 2.2+ 已安装并运行
- **GNS3服务器** 可访问：`http://localhost:3080`
- **Python 3.8+**
- **DeepSeek API密钥**（可选，用于增强AI功能）
- 至少一个**GNS3项目**包含网络设备（推荐使用Cisco IOSv设备）

## 🛠 快速安装

```bash
# 1. 克隆仓库
git clone https://github.com/yueguobin/gns3-copilot.git
cd gns3-copilot

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 设置环境变量（可选）
echo "DEEPSEEK_API_KEY=your_api_key_here" > .env
```

## 🎯 快速开始

```bash
# 1. 启动GNS3并打开项目
# 2. 运行助手
chainlit run gns3_copilot.py

# 3. 浏览器访问显示的URL（通常是 http://localhost:8000）
# 4. 在聊天界面使用自然语言命令
```

## 💬 命令示例

### 显示操作
- `"检查R-1和R-2接口状态"`
- `"显示R-3和R-4的OSPF状态"`
- `"显示R-1运行配置"`

### 配置操作
- `"在R-3上配置环回接口地址3.3.3.31/32"`
- `"在R-1上启用OSPF"`
- `"设置R-2的GigabitEthernet0/0接口描述"`

### 拓扑操作
- `"显示当前拓扑"`
- `"列出项目中所有设备"`
- `"启动所有节点"`

### 创建实验
- `"创建包含六个路由器的拓扑，测试多区域OSPF，配置主机名为设备名"`

## 🛡 安全特性

- **命令验证**：防止执行危险命令
- **只读模式**：显示和配置操作分离
- **错误处理**：全面错误报告和恢复
- **操作日志**：所有操作记录用于审计

**禁止命令**：系统拒绝执行`reload`、`write erase`、`erase startup-config`等破坏性操作。

## 🏗 架构概览

```
GNS3 Copilot
├── Web界面 (Chainlit)
├── AI智能体 (LangChain + DeepSeek)
├── 工具系统
│   ├── GNS3拓扑读取器
│   ├── 多设备命令执行器 (Nornir)
│   ├── 多设备配置执行器 (Nornir)
│   ├── 单设备配置执行器
│   ├── 节点管理工具
│   ├── 链路管理工具
│   └── 节点控制工具
└── GNS3 API集成
```

## 📁 项目结构

```
gns3-copilot/
├── gns3_copilot.py          # 主应用程序
├── requirements.txt         # 依赖包
├── LICENSE                  # MIT许可证
├── .env                    # 环境变量（可选）
├── README.md               # 英文文档
├── README_ZH.md            # 本文件（中文文档）
├── chainlit.md             # Chainlit界面文档
├── log/                    # 应用日志
├── reports/                # 过程分析器文档输出
├── process_analyzer/       # 过程分析模块
├── prompts/                # AI提示模板
├── tools/                  # 工具实现
└── docs/                   # 额外文档
```

## 🐛 故障排除

### 常见问题

1. **GNS3服务器连接被拒绝**
   - 确保GNS3服务器运行在`localhost:3080`
   - 检查防火墙设置

2. **拓扑中找不到设备**
   - 验证设备名称完全匹配
   - 确保设备配置了控制台端口

3. **命令执行超时**
   - 检查设备响应性
   - 根据需要增加超时设置

### 日志文件

检查`log/`目录获取详细操作日志：
- `gns3_copilot.log` - 主应用日志和会话管理
- `config_tools_nornir.log` - 多设备配置命令执行（Nornir基础）
- `display_tools_nornir.log` - 多设备显示命令执行（Nornir基础）
- `gns3_topology_reader.log` - GNS3拓扑发现和API交互
- 其他工具专用日志文件

## 📚 更多文档

- **[API参考](docs/API_REFERENCE.md)** - 完整API文档
- **[贡献指南](docs/CONTRIBUTING.md)** - 开发贡献指南
- **[过程分析器](process_analyzer/README.md)** - 过程分析模块文档

## 📄 许可证

本项目采用 [MIT许可证](LICENSE) 开源。

## 🙏 致谢

- **GNS3团队** - 优秀的网络仿真平台
- **LangChain** - 强大的AI智能体框架
- **DeepSeek** - AI语言模型能力
- **Chainlit** - 对话式UI框架
- **Netmiko** - 网络设备通信
- **Nornir** - 并发多设备自动化

---

**版本**: 1.0.0 - 稳定版本，完整功能支持

## 🌟 中文支持

本文档为GNS3 Copilot的中文版本，提供：

- 完整的中文安装和使用指南
- 中文命令示例和说明
- 中文故障排除指南
- 本地化的用户体验

如果您更习惯使用中文文档，可以参考本文件。对于技术细节和API参考，建议同时查看英文版本文档以获取最新信息。
