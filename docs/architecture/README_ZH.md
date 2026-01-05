# GNS3 Copilot 架构文档

本目录包含GNS3 Copilot的系统架构和框架设计文档。

## 文档索引

### 核心架构文档

- **[系统架构](system-architecture_ZH.md)** - GNS3 Copilot系统架构全面概览，包括所有层次及其交互
- **[核心框架设计](core-framework-design_ZH.md)** - LangGraph智能体框架、LangChain工具集成框架和数据流架构的详细设计

## 架构图

所有架构图和流程图位于 [images/](images/) 目录：

### Mermaid/SVG图表
- `gns3_copilot_architecture.svg` - 完整系统架构图
- `framework-data-flow.svg` - 组件间数据流
- `langchain-tools.svg` - LangChain工具集成框架
- `langgraph-agent.svg` - LangGraph智能体框架
- `multi-agent.svg` - 多智能体系统架构

### 截图
- `config-first-party.jpeg` - 第一方提供商配置
- `config-third-party.jpeg` - 第三方提供商配置
- `gns3-select-project.jpeg` - GNS3项目选择界面

## 架构概览

GNS3 Copilot采用**7层架构**：

1. **表示层** - Streamlit Web界面
2. **LangGraph智能体框架** - AI编排和状态管理
3. **工具集成层** - 网络自动化工具
4. **网络自动化框架** - 基于Nornir的并发执行
5. **GNS3集成框架** - 自定义GNS3 API客户端
6. **数据持久层** - SQLite数据库和日志系统
7. **基础设施层** - GNS3服务器和网络设备

## 核心框架

- **LangGraph** - 状态机工作流和智能体编排
- **LangChain** - 工具集成和LLM抽象
- **Nornir** - 高性能并发网络自动化
- **Streamlit** - Web UI框架

## 快速参考

### 系统组件
- **智能体**: 包含规划、执行、监督和专家智能体的多智能体系统
- **工具**: 9个专用工具用于GNS3管理和网络自动化
- **状态管理**: 基于SQLite的检查点机制实现对话持久化
- **执行**: 通过Nornir线程池实现并发设备操作

### 数据流
1. 用户输入 → Streamlit UI
2. LangGraph StateGraph处理输入
3. LLM决定调用哪些工具
4. 工具通过Nornir/GNS3客户端执行网络操作
5. 结果通过智能体流回UI
6. 对话状态通过SQLite检查点持久化

## 相关文档

- [常见问题](../user/FAQ_ZH.md) - 系统常见问题
- [测试指南](../development/testing/manual_testing_guide_zh.md) - 如何测试架构
- [后端演进计划](../development/evolution/GNS3-Copilot-Backend-Evolution-Plan_ZH.md) - 未来路线图
