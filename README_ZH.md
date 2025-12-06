# GNS3 Copilot

一个基于AI的网络自动化助手，专为GNS3网络模拟器设计，提供智能化的网络设备管理和自动化操作。

## 项目简介

GNS3 Copilot 是一个强大的网络自动化工具，集成了多种AI模型和网络自动化框架，能够通过自然语言与用户交互，执行网络设备配置、拓扑管理和故障诊断等任务。

<img src="https://raw.githubusercontent.com/yueguobin/gns3-copilot/refs/heads/master/demo.gif" alt="GNS3 Copilot 功能演示" width="1280"/>


### 核心功能

- 🤖 **AI驱动的对话界面**: 支持自然语言交互，理解网络自动化需求
- 🔧 **设备配置管理**: 批量配置网络设备，支持多种厂商设备（目前仅测试了Cisco IOSv镜像）
- 📊 **拓扑管理**: 自动创建、修改和管理GNS3网络拓扑
- 🔍 **网络诊断**: 智能网络故障排查和性能监控
- 🌐 **LLM支持**: 集成DeepSeek AI模型进行自然语言处理




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
- GNS3 Server (运行在 http://localhost:3080或远程主机)
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

1. **启动GNS3 Server**
确保GNS3 Server运行并可以通过网络访问其API接口：`http://x.x.x.x:3080`

## 使用指南

### 启动

```bash
# 启动Streamlit Web界面
streamlit run app.py

# Web界面将在 http://localhost:8501 打开
# 提供直观的图形界面与AI代理交互
```
### 在设置页面进行配置

**使用First-Party Providers配置**

![First-Party Providers](https://github.com/yueguobin/gns3-copilot/blob/master/Config_First-Party.jpeg?raw=true)

**使用Third-Party Aggregators配置**

![Third-Party Aggregators](https://github.com/yueguobin/gns3-copilot/blob/master/Config_Third-Party-Aggregator.jpeg?raw=true)

### 配置参数详解

#### 📋 配置文件概述

GNS3 Copilot 的配置通过 Streamlit 界面管理，所有设置保存在项目根目录的 `.env` 文件中。首次运行时如果 `.env` 文件不存在，系统会自动创建。

#### 🔧 主要配置内容

##### 1. GNS3 服务器配置
- **GNS3 Server Host**: GNS3 服务器主机地址（如：127.0.0.1）
- **GNS3 Server URL**: GNS3 服务器完整 URL（如：http://127.0.0.1:3080）
- **API Version**: GNS3 API 版本（支持 v2 和 v3，目前仅支持v2， v3接口测试中。）
- **GNS3 Server Username**: GNS3 服务器用户名（仅 API v3 需要）
- **GNS3 Server Password**: GNS3 服务器密码（仅 API v3 需要）

##### 2. LLM 模型配置
- **Model Provider**: 模型提供商（支持：openai, anthropic, deepseek, xai, openrouter 等）
- **Model Name**: 具体模型名称（如：deepseek-chat, gpt-4o-mini 等）
- **Model API Key**: 模型 API 密钥
- **Base URL**: 模型服务的基础 URL（使用 OpenRouter 等第三方平台时必需）
- **Temperature**: 模型温度参数（控制输出随机性，范围 0.0-1.0）

##### 3. 其他设置
- **Linux Console Username**: Linux 控制台用户名（用于 GNS3 中的 Debian 设备）
- **Linux Console Password**: Linux 控制台密码

#### ⚠️ 重要注意事项

##### 1. 配置文件管理
- 配置自动保存在项目根目录的 `.env` 文件中
- 如果 `.env` 文件不存在，系统会自动创建
- 首次运行时会显示警告提示配置文件已创建

##### 2. API 版本兼容性
- **API v2**: 不需要用户名和密码认证
- **API v3**: 必须提供用户名和密码进行认证
- 系统会根据选择的 API 版本动态显示/隐藏认证字段

##### 3. 模型配置要点
- **OpenRouter 平台使用**：
  - Model Provider 应填写 "openai"
  - Base URL 必须填写：`https://openrouter.ai/api/v1`
  - Model Name 格式：`openai/gpt-4o-mini` 或 `x-ai/grok-4-fast`

##### 4. 安全注意事项
- API Key 字段使用密码类型输入，内容会被隐藏
- 建议定期更换 API 密钥
- 不要将 `.env` 文件提交到版本控制系统

##### 5. 配置验证
- 系统会对配置项进行基本验证：
  - API 版本只能是 "2" 或 "3"
  - Model Provider 必须在支持的列表中
  - Temperature 必须是有效的数字格式

##### 6. Linux 设备配置
- 用户名和密码用于连接 GNS3 中的 Debian Linux 设备
- 默认示例用户名和密码都是 "debian"
- 需要确保 GNS3 中已正确配置 Debian 设备

#### 🚀 使用建议

1. **首次配置**：按照界面提示逐项填写，带 `*` 的为必填项
2. **测试连接**：配置完成后建议先测试 GNS3 服务器连接
3. **模型选择**：根据需求选择合适的模型提供商和具体模型
4. **备份配置**：定期备份 `.env` 文件以防配置丢失


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
