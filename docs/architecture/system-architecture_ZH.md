graph TB
    %% 表示层
    subgraph "表示层"
        StreamlitUI[Streamlit Web界面]
        ChatInterface[聊天界面]
        SettingsPage[设置页面]
        HelpPage[帮助页面]
        SessionManager[会话管理]
    end

    %% LangGraph智能体框架
    subgraph "LangGraph智能体框架"
        StateGraph[StateGraph工作流]
        LLMNode[llm_call节点]
        ToolNode[tool_node节点]
        TitleNode[title_generator节点]
        %% 路由逻辑
        ShouldContinueRouter[should_continue路由器]
        RecursionRouter[recursion_limit_continue路由器]
        %% 状态管理
        MessagesState[MessagesState]
        SQLiteCheckpoint[SQLite检查点]
    end

    %% 工具集成层
    subgraph "工具集成层"
        GNS3TemplateTool[GNS3模板工具]
        GNS3TopologyTool[GNS3拓扑工具]
        GNS3CreateNodeTool[GNS3创建节点工具]
        GNS3LinkTool[GNS3连接工具]
        GNS3StartNodeTool[GNS3启动节点工具]
        ExecuteDisplayCommands[执行显示命令]
        ExecuteConfigCommands[执行配置命令]
        VPCSMultiCommands[VPCS多命令]
        LinuxTelnetBatch[Linux Telnet批量]
    end

    %% 网络自动化框架
    subgraph "网络自动化框架"
        NornirEngine[Nornir并发引擎]
        NetmikoConnector[Netmiko连接器]
        Telnetlib3Client[Telnetlib3客户端]
        DeviceInventory[设备清单]
        ThreadPool[线程池执行器]
    end

    %% GNS3集成框架
    subgraph "GNS3集成框架"
        CustomGNS3Client[自定义GNS3客户端]
        GNS3Connector[GNS3 API连接器]
        ProjectManager[项目管理器]
        NodeManager[节点管理器]
        LinkManager[连接管理器]
        TopologyReader[拓扑读取器]
    end

    %% 数据持久层
    subgraph "数据持久层"
        SQLiteDB[(SQLite数据库)]
        LogFiles[日志文件]
        ConfigFiles[配置文件]
        CheckpointDB[检查点数据库]
    end

    %% 基础设施层
    subgraph "基础设施层"
        GNS3Server[GNS3服务器]
        NetworkDevices[网络设备]
        VirtualMachines[虚拟机]
        NetworkTopology[网络拓扑]
    end

    %% 数据流连接
    %% UI到智能体
    StreamlitUI --> ChatInterface
    ChatInterface --> StateGraph
    SettingsPage --> ConfigFiles
    SessionManager --> SQLiteCheckpoint
    %% LangGraph内部流程
    StateGraph --> LLMNode
    LLMNode --> ShouldContinueRouter
    ShouldContinueRouter --> ToolNode
    ShouldContinueRouter --> TitleNode
    ToolNode --> RecursionRouter
    RecursionRouter --> LLMNode
    TitleNode --> SQLiteCheckpoint
    %% 状态管理
    MessagesState --> StateGraph
    SQLiteCheckpoint --> MessagesState
    %% 工具集成
    ToolNode --> GNS3TemplateTool
    ToolNode --> GNS3TopologyTool
    ToolNode --> GNS3CreateNodeTool
    ToolNode --> GNS3LinkTool
    ToolNode --> GNS3StartNodeTool
    ToolNode --> ExecuteDisplayCommands
    ToolNode --> ExecuteConfigCommands
    ToolNode --> VPCSMultiCommands
    ToolNode --> LinuxTelnetBatch
    %% 工具到自动化框架
    ExecuteDisplayCommands --> NornirEngine
    ExecuteConfigCommands --> NornirEngine
    VPCSMultiCommands --> Telnetlib3Client
    LinuxTelnetBatch
    Telnetlib3Client
    %% 自动化框架内部
    NornirEngine --> NetmikoConnector
    NornirEngine --> DeviceInventory
    NornirEngine
    ThreadPool
    Telnetlib3Client --> DeviceInventory
    %% 工具到GNS3框架
    GNS3TemplateTool --> CustomGNS3Client
    GNS3TopologyTool --> CustomGNS3Client
    GNS3CreateNodeTool --> CustomGNS3Client
    GNS3LinkTool --> CustomGNS3Client
    GNS3StartNodeTool --> CustomGNS3Client
    %% GNS3框架内部
    CustomGNS3Client --> GNS3Connector
    CustomGNS3Client --> ProjectManager
    CustomGNS3Client --> NodeManager
    CustomGNS3Client --> LinkManager
    CustomGNS3Client --> TopologyReader
    %% 持久化连接
    SQLiteCheckpoint --> CheckpointDB
    StateGraph --> LogFiles
    StreamlitUI --> ConfigFiles
    %% 基础设施连接
    GNS3Connector --> GNS3Server
    NetmikoConnector --> NetworkDevices
    Telnetlib3Client
    NetworkDevices
    TopologyReader --> NetworkTopology
    NodeManager --> VirtualMachines

    %% 样式定义
    classDef presentation fill:#e3f2fd,stroke:#1565c0,stroke-width:3px
    classDef agent fill:#f3e5f5,stroke:#7b1fa2,stroke-width:3px
    classDef tools fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef automation fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    classDef gns3 fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef persistence fill:#f1f8e9,stroke:#689f38,stroke-width:2px
    classDef infrastructure fill:#e0f2f1,stroke:#00695c,stroke-width:2px
    class StreamlitUI,ChatInterface,SettingsPage,HelpPage,SessionManager presentation
    class StateGraph,LLMNode,ToolNode,TitleNode,ShouldContinueRouter,RecursionRouter,MessagesState,SQLiteCheckpoint agent
    class GNS3TemplateTool,GNS3TopologyTool,GNS3CreateNodeTool,GNS3LinkTool,GNS3StartNodeTool,ExecuteDisplayCommands,ExecuteConfigCommands,VPCSMultiCommands,LinuxTelnetBatch tools
    class NornirEngine,NetmikoConnector,Telnetlib3Client,DeviceInventory,ThreadPool automation
    class CustomGNS3Client,GNS3Connector,ProjectManager,NodeManager,LinkManager,TopologyReader gns3
    class SQLiteDB,LogFiles,ConfigFiles,CheckpointDB persistence
    class GNS3Server,NetworkDevices,VirtualMachines,NetworkTopology infrastructure
	LinuxTelnetBatch --- NornirEngine
	ProjectManager --- GNS3Server
	LinkManager --- NetworkTopology
	Telnetlib3Client --- ThreadPool
	ThreadPool --- NetworkDevices
	DeviceInventory
	TopologyReader
	CheckpointDB --- SQLiteDB
	subGraph2
	LogFiles
```


# GNS3 Copilot 系统架构

## 概述

GNS3 Copilot是一个基于AI的网络自动化助手，与GNS3网络模拟器集成，提供智能化的网络管理和自动化能力。系统采用多层架构，具有清晰的职责分离，能够实现可扩展和可维护的网络自动化解决方案。

## 架构层次

### 1. 表示层

**Streamlit Web界面**：提供直观交互的现代基于Web的UI
- **聊天界面**：用于自然语言交互的实时对话界面
- **设置页面**：LLM提供商、GNS3连接和系统参数的配置管理
- **帮助页面**：文档和用户指导
- **会话管理**：支持多会话，包括对话历史和持久化

### 2. LangGraph智能体框架

**StateGraph工作流**：使用LangGraph的核心AI智能体编排
- **llm_call节点**：处理LLM推理和决策
- **tool_node节点**：基于LLM决策执行工具调用
- **title_generator节点**：生成对话标题用于会话标识
- **路由逻辑**：
  - `should_continue`：确定是否需要工具执行或对话继续
  - `recursion_limit_continue`：通过步骤限制防止无限循环
- **状态管理**：
  - `MessagesState`：维护对话历史和上下文
  - `SQLite检查点`：对话连续性的持久化状态存储

### 3. 工具集成层

8个专用工具，实现全面的网络自动化：

**GNS3管理工具**：
- **GNS3模板工具**：从GNS3服务器获取可用节点模板
- **GNS3拓扑工具**：读取和分析网络拓扑信息
- **GNS3创建节点工具**：在GNS3项目中创建新的网络节点
- **GNS3连接工具**：在网络节点之间建立连接
- **GNS3启动节点工具**：管理节点生命周期（启动/停止/重启）

**网络自动化工具**：
- **执行显示命令**：同时在多个设备上运行显示/查看命令
- **执行配置命令**：在多个设备上应用配置更改
- **VPCS多命令**：管理虚拟PC模拟器实例
- **Linux Telnet批量**：通过Telnet在Linux设备上执行批量命令

### 4. 网络自动化框架

**Nornir并发引擎**：高性能自动化框架
- **Netmiko连接器**：网络设备的SSH/Telnet连接
- **Telnetlib3客户端**：用于VPCS和Linux设备的异步Telnet客户端
- **设备清单**：动态设备发现和管理
- **线程池执行器**：并发执行以提高性能

### 5. GNS3集成框架

**自定义GNS3客户端**：基于gns3fy的增强型GNS3 API客户端
- **GNS3 API连接器**：与GNS3服务器的RESTful API通信
- **项目管理器**：GNS3项目生命周期管理
- **节点管理器**：节点配置和控制操作
- **连接管理器**：网络连接管理
- **拓扑读取器**：网络拓扑分析和可视化

### 6. 数据持久层

**SQLite数据库**：轻量级、可靠的数据存储
- **检查点数据库**：LangGraph对话状态持久化
- **日志文件**：全面的系统活动日志记录
- **配置文件**：系统和用户首选项管理

### 7. 基础设施层

**网络基础设施**：物理和虚拟网络组件
- **GNS3服务器**：网络模拟和仿真平台
- **网络设备**：路由器、交换机、防火墙和其他网络设备
- **虚拟机**：用于网络测试的来宾操作系统实例
- **网络拓扑**：逻辑和物理网络布局

## 数据流和交互

### 对话流程
1. 用户输入通过Streamlit聊天界面进入
2. LangGraph StateGraph通过llm_call节点处理输入
3. 路由逻辑确定是否需要工具执行
4. 工具执行适当的网络操作
5. 结果通过智能体流回用户界面
6. 对话状态通过SQLite检查点持久化

### 工具执行流程
1. LLM分析用户意图并选择适当的工具
2. 工具节点使用提供的参数执行选定的工具
3. 网络自动化框架处理设备连接
4. GNS3集成框架管理模拟器操作
5. 结果被格式化并返回到对话中

### 会话管理
1. 每个对话会话获得唯一的线程ID
2. SQLite检查点维护跨会话的对话状态
3. 会话历史允许对话继续
4. 标题生成提供有意义的会话标识

## 技术规格

### 支持的LLM提供商
- OpenAI（GPT模型）
- Anthropic（Claude模型）
- Google（Gemini模型）
- AWS（Bedrock模型）
- Ollama（本地模型）
- DeepSeek
- XAI（Grok模型）

### 网络设备支持
- Cisco IOS/IOS-XE/NX-OS
- Juniper Junos
- Arista EOS
- Linux系统
- VPCS（虚拟PC模拟器）
- 通过Netmiko支持自定义设备类型

### GNS3集成
- GNS3 Server 2.2+
- 所有节点类型（路由器、交换机、主机等）
- 项目和拓扑管理
- 实时节点控制
- 连接管理

### 性能特性
- 通过Nornir实现并发设备执行
- 异步Telnet操作
- 线程池优化
- 高效的状态管理
- 用于实时交互的流式响应

## 安全性和可靠性

### 安全措施
- 通过环境变量管理API密钥
- 安全的凭据存储
- 网络隔离选项
- 通过GNS3权限进行访问控制

### 可靠性特性
- 健壮的错误处理和恢复
- 连接超时管理
- 状态持久化和恢复
- 用于故障排除的综合日志记录
- 服务故障时的优雅降级

## 可扩展性考虑

### 水平扩展
- 无状态智能体设计
- 分布式检查点存储
- 负载均衡器兼容性
- 微服务架构潜力

### 垂直扩展
- 可配置的线程池
- 内存高效的状态管理
- 优化的数据库操作
- 资源监控能力

此架构为基于AI的网络自动化提供了坚实的基础，同时保持了对未来增强和集成的灵活性。
