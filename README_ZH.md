# GNS3 Copilot

[![CI - QA & Testing](https://github.com/yueguobin/gns3-copilot/actions/workflows/ci.yaml/badge.svg)](https://github.com/yueguobin/gns3-copilot/actions/workflows/ci.yaml)
[![CD - Production Release](https://github.com/yueguobin/gns3-copilot/actions/workflows/cd.yaml/badge.svg)](https://github.com/yueguobin/gns3-copilot/actions/workflows/cd.yaml)
[![codecov](https://codecov.io/gh/yueguobin/gns3-copilot/branch/Development/graph/badge.svg?token=7FDUCM547W)](https://codecov.io/gh/yueguobin/gns3-copilot)
[![PyPI version](https://img.shields.io/pypi/v/gns3-copilot)](https://pypi.org/project/gns3-copilot/)
[![PyPI downloads](https://static.pepy.tech/badge/gns3-copilot)](https://pepy.tech/project/gns3-copilot)
![License](https://img.shields.io/badge/license-MIT-green.svg) 
[![platform](https://img.shields.io/badge/platform-linux%20%7C%20windows%20%7C%20macOS-lightgrey)](https://shields.io/)

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

[GNS3-Copilot Architecture](Architecture/gns3_copilot_architecture.md)

[Core Framework Detailed Design](Architecture/Core%20Framework%20Detailed%20Design.md)


最终概念：多智能体系统架构和动态上下文管理器（基于当前的理解）

**多智能体角色分配**

该系统采用不同的智能体，每个智能体专门负责特定功能：

- **规划智能体（Planning Agent）**：负责**识别用户意图**并**制定详细任务计划**。
    
- **执行智能体（Execution Agent）**：负责根据计划**逐步执行具体设备操作**。
    
- **监督智能体（Supervision Agent）**：负责**持续监控**和评估执行智能体的结果。如果发现问题，它会要求执行智能体**重试**或通知**专家智能体**介入。
    
- **专家智能体（Expert Agent）**：负责解决监督智能体发现的复杂问题，提供**指导**、**纠正计划**或**提出解决方案**。
    

**系统工作流程**

该过程以闭环结构运行，确保可靠性和自我纠正：

1. **用户输入请求**
    
    - 用户通过提交任务或请求启动系统。
        
2. **规划智能体：意图识别和计划制定**
    
    - 规划智能体分析请求，理解目标，并生成执行步骤序列。
        
3. **执行智能体：执行计划步骤**
    
    - 执行智能体获取计划步骤并执行相应的具体操作。
        
4. **监督智能体：实时监控和评估**
    
    - 监督智能体持续检查每个执行步骤的结果。
        
    - **检测到问题** $\rightarrow$ 要求执行智能体**重试**或**通知专家智能体**。
        
5. **专家智能体：干预和指导/纠正**
    
    - 当报告复杂问题时，专家智能体介入。
        
    - 它提供指导 $\rightarrow$ **纠正计划**（循环回到步骤2）或**提出解决方案**（循环回到步骤3）。
        
6. **返回最终工作结果**
    
    - 一旦所有步骤成功完成并验证，最终结果将交付给用户。


## 安装指南

### 环境要求

- Python 3.10+
- GNS3 Server (运行在 http://localhost:3080或远程主机)
- 支持的操作系统: Windows, macOS, Linux

### 安装步骤

1. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows
```

2. **安装 GNS3 Copilot**
```bash
pip install gns3-copilot
```

3. **启动 GNS3 Server**
确保 GNS3 Server 运行并可以通过网络访问其 API 接口：`http://x.x.x.x:3080`

4. **启动应用程序**
```bash
gns3-copilot
```


## 使用指南

### 启动

```bash
# 基本启动，默认端口8501
gns3-copilot

# 指定自定义端口
gns3-copilot --server.port 8080

# 指定地址和端口
gns3-copilot --server.address 0.0.0.0 --server.port 8080

# 无头模式运行
gns3-copilot --server.headless true

# 获取帮助
gns3-copilot --help

```


### 配置参数详解


#### 🔧 主要配置内容

##### 1. GNS3 服务器配置
- **GNS3 Server Host**: GNS3 服务器主机地址（如：127.0.0.1）
- **GNS3 Server URL**: GNS3 服务器完整 URL（如：http://127.0.0.1:3080）
- **API Version**: GNS3 API 版本（支持 v2 和 v3）
- **GNS3 Server Username**: GNS3 服务器用户名（仅 API v3 需要）
- **GNS3 Server Password**: GNS3 服务器密码（仅 API v3 需要）

##### 2. LLM 模型配置
- **Model Provider**: 模型提供商（支持：openai, anthropic, deepseek, xai, openrouter 等）
- **Model Name**: 具体模型名称（如：deepseek-chat, gpt-4o-mini 等）
- **Model API Key**: 模型 API 密钥
- **Base URL**: 模型服务的基础 URL（使用 OpenRouter 等第三方平台时必需）
- **Temperature**: 模型温度参数（控制输出随机性，范围 0.0-1.0）

##### 3. 语音功能配置
- **Voice Features**: 语音功能开关（启用/禁用TTS/STT功能）
- **TTS API Key**: 文本转语音服务API密钥
- **TTS Model**: TTS模型选择（支持：tts-1, tts-1-hd, gpt-4o-mini-tts）
- **TTS Voice**: 语音角色选择（支持：alloy, ash, ballad等）
- **TTS Speed**: 语音播放速度（范围：0.25-4.0）
- **TTS Base URL**: TTS服务基础URL
- **STT API Key**: 语音转文本服务API密钥
- **STT Model**: STT模型选择（支持：whisper-1, gpt-4o-transcribe等）
- **STT Language**: 识别语言代码（如：en, zh, ja）
- **STT Temperature**: 识别温度参数（控制随机性，范围0.0-1.0）
- **STT Response Format**: 输出格式（支持：json, text, srt等）
- **STT Base URL**: STT服务基础URL

##### 4. 其他设置
- **Linux Console Username**: Linux 控制台用户名（用于 GNS3 中的 Debian 设备）
- **Linux Console Password**: Linux 控制台密码


## 安全注意事项

**API密钥保护**: 
   - 不要将 `.env` 文件提交到版本控制
   - 定期轮换API密钥
   - 使用最小权限原则


## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## Acknowledgements

Special thanks to the following resources for their inspiration and technical foundation:

* **Powered by 《网络工程师的 Python 之路》**
* **Powered by 《网络工程师的 AI 之路》**


## 联系方式

- 项目主页: https://github.com/yueguobin/gns3-copilot
- 问题反馈: https://github.com/yueguobin/gns3-copilot/issues


---
