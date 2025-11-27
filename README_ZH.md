# GNS3 Copilot

一个基于AI的网络自动化助手，专为GNS3网络模拟器设计，提供智能化的网络设备管理和自动化操作。

## 项目简介

GNS3 Copilot 是一个强大的网络自动化工具，集成了多种AI模型和网络自动化框架，能够通过自然语言与用户交互，执行网络设备配置、拓扑管理和故障诊断等任务。

### 核心功能

- 🤖 **AI驱动的对话界面**: 支持自然语言交互，理解网络自动化需求
- 🔧 **设备配置管理**: 批量配置网络设备，支持多种厂商设备（目前仅测试了Cisco IOSv镜像）
- 📊 **拓扑管理**: 自动创建、修改和管理GNS3网络拓扑
- 🔍 **网络诊断**: 智能网络故障排查和性能监控
- 🌐 **LLM支持**: 集成DeepSeek AI模型进行自然语言处理


<img src="assets/demo.gif" alt="GNS3 Copilot 功能演示" width="1280"/>


## 技术架构

### 核心组件

- **Agent Framework**: 基于LangChain v1.0.7和LangGraph构建的智能代理系统
- **Network Automation**: 使用Nornir v3.5.0和Netmiko v4.6.0进行网络设备自动化
- **GNS3 Integration**: 自定义GNS3 API客户端，支持拓扑和节点管理，具备JWT认证功能
- **AI Models**: 支持DeepSeek Chat大语言模型

### 工具集

| 工具名称 | 功能描述 |
|---------|---------|
| `GNS3TopologyTool` | 读取GNS3拓扑信息 |
| `GNS3CreateNodeTool` | 创建GNS3节点 |
| `GNS3LinkTool` | 创建节点间连接 |
| `GNS3StartNodeTool` | 启动GNS3节点 |
| `GNS3TemplateTool` | 获取节点模板 |
| `ExecuteMultipleDeviceCommands` | 执行显示命令 |
| `ExecuteMultipleDeviceConfigCommands` | 执行配置命令 |
| `VPCSMultiCommands` | 在多个设备上执行VPCS命令 |
| `LinuxTelnetBatchTool` | 在多个设备上执行linux命令 |

## 安装指南

### 环境要求

- Python 3.8+
- GNS3 Server (运行在 http://localhost:3080)
- 支持的操作系统: Windows, macOS, Linux

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/yueguobin/gns3-copilot.git
cd gns3-copilot
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
pip install .
```

4. **配置环境变量**
复制环境变量模板并配置您的设置：
```bash
cp env.example .env
```

编辑 `.env` 文件并配置您的设置：
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

5. **启动GNS3 Server**
确保GNS3 Server运行在默认地址 `http://localhost:3080`

## 使用指南

### 启动方式


#### 方式2: Streamlit Web UI

```bash
# 启动Streamlit Web界面
streamlit run app.py

# Web界面将在 http://localhost:8501 打开
# 提供直观的图形界面与AI代理交互
```


## 配置说明

### GNS3 Server配置

确保GNS3 Server正确配置：
- 默认端口: 3080
- 启用HTTP API
- 配置适当的模拟器镜像
- GNS3 SERVER API v3（JWT认证）API(测试中)

### 日志配置

项目使用统一的日志系统，日志文件保存在 `log/` 目录：
- `gns3_copilot.log`: 主应用日志
- `display_tools_nornir.log`: 查看类命令工具日志
- `config_tools_nornir.log`: 配置类命令工具日志

### AI模型配置

支持多种AI模型，在 `agent/gns3_copilot.py` 中配置：

```python
# 主要模型 (DeepSeek)
base_model = init_chat_model(
    model="deepseek-chat",
    temperature=0
)

# 辅助模型 (Google Gemini)
assist_model = init_chat_model(
    model="google_genai:gemini-2.5-flash",
    temperature=0
)
```

**说明**: 系统使用DeepSeek作为主要LLM进行自然语言处理，Google Gemini作为辅助模型提供增强功能。

## 安全注意事项

⚠️ **重要安全提示**：

1. **配置命令安全**: 配置工具具有修改设备配置的能力，使用前请确保：
   - 在测试环境中验证
   - 备份重要配置
   - 了解每个命令的作用

2. **API密钥保护**: 
   - 不要将 `.env` 文件提交到版本控制
   - 定期轮换API密钥
   - 使用最小权限原则

3. **网络隔离**: 建议在隔离的测试环境中使用

## 故障排除

### 常见问题

1. **GNS3连接失败**
   - 检查GNS3 Server是否运行
   - 确认端口3080是否可访问
   - 检查防火墙设置

2. **设备连接问题**
   - 确认设备控制台端口正确
   - 检查设备是否已启动
   - 验证Telnet连接

3. **AI模型调用失败**
   - 检查API密钥是否正确
   - 确认网络连接
   - 验证API配额

4. **认证问题**
   - 对于GNS3 v3，确保JWT令牌正确配置(测试中)
   - 检查环境变量中的API凭据

### 调试模式

启用详细日志：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

- 项目主页: https://github.com/yueguobin/gns3-copilot
- 问题反馈: https://github.com/yueguobin/gns3-copilot/issues


---

**免责声明**: 本工具仅用于教育和测试目的。在生产环境中使用前，请充分测试并确保符合您的安全策略。
