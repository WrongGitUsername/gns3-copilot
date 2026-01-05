# FAQ - GNS3 Copilot 常见问题

本文档收集了 GNS3 Copilot 使用过程中的常见问题及解决方案。

---

## 修改 GNS3 Server 配置后，Chat 页面无法获取到新的地址

### 问题描述

在 Settings 页面修改了 GNS3 Server URL 或其他配置后，点击保存并切换到 Chat 页面，发现 Show 按钮显示的拓扑 iframe 仍使用旧的 GNS3 Server 地址，而不是新配置的地址。这也适用于 LLM 模型配置的修改。

### 原因分析

这是由于 Streamlit 的 Widget 行为机制导致的：

1. **Widget 不会在页面间保持状态**
   - 即使 key 相同，不同页面上的 widget 也被视为不同实例
   - Settings 页面的 widget key（如 `key="GNS3_SERVER_URL"`）在切换页面后会被 Streamlit 自动删除

2. **Widget 执行时才会保持状态**
   - 如果 widget 在某次运行中没有被调用，它的所有信息（包括 session_state 中的 key）都会被删除

3. **配置加载机制**
   - `load_config_from_env()` 函数使用 `_config_loaded` 标志来避免重复加载
   - 首次加载后设置为 `True`，后续切换页面时不会重新加载
   - 切换页面后，widget key 被删除，但 `_config_loaded` 仍为 `True`
   - 结果：Chat 页面读取不到新的配置值

### 完整的问题流程

```
1. 首次启动
   ├─ load_config_from_env() 执行
   ├─ 从 .env 加载配置到 session_state
   └─ 设置 _config_loaded = True

2. 用户在 Settings 页面修改配置
   ├─ widget 覆盖 session_state 中的值
   ├─ 点击保存按钮
   ├─ save_config_to_env() 保存到 .env 文件
   └─ 执行 st.rerun()

3. 切换到 Chat 页面
   ├─ app.py 重新执行
   ├─ Settings 页面的 widget 不再执行
   ├─ Streamlit 删除 widget key（GNS3_SERVER_URL 等）
   ├─ load_config_from_env() 检查 _config_loaded = True
   ├─ 跳过配置加载
   └─ Chat 页面读取不到新配置，使用默认值
```

### 解决方案

**当前方案**：重启应用程序

修改 GNS3 Server 配置或 LLM 模型设置后，必须**重启应用程序**才能使更改生效。重启应用程序会：

1. 清除 session_state（包括 `_config_loaded` 标志）
2. app.py 从头重新执行
3. `load_config_from_env()` 从 .env 文件重新加载配置
4. Chat 页面获取到最新的配置值

**操作步骤**：
```
1. 在 Settings 页面修改配置并保存
2. 停止 gns3-copilot 进程
3. 重新启动应用程序
4. 配置已生效
```

**重要提示**：
- **LLM 模型配置的修改需要重启应用程序**
- **GNS3 服务器配置的修改需要重启应用程序**
- 仅刷新浏览器页面（按 F5）无法使配置生效

### 工作建议

- 首次配置好 GNS3 Server 地址和 LLM 模型后，验证配置是否正常工作再继续
- 如果确实需要修改配置，请重启应用程序以确保所有更改生效
- 每次重启后测试配置以确认其正常工作


### 相关代码位置

- 配置加载逻辑：`src/gns3_copilot/ui_model/utils/config_manager.py`
  - `load_config_from_env()` - 加载配置
  - `save_config_to_env()` - 保存配置

- Settings 页面：`src/gns3_copilot/ui_model/settings.py`
  - 配置输入框（使用 widget key）

- Chat 页面：`src/gns3_copilot/ui_model/chat.py`
  - `build_topology_iframe_url()` - 构建 GNS3 拓扑 iframe URL
  - 读取 GNS3_SERVER_URL 等 session_state 配置

### 参考资料

- [Streamlit Widget Behavior](https://docs.streamlit.io/library/advanced-features/widget-behavior)
- Streamlit 官方文档关于 Widget 状态管理的说明

---

## 项目背景和架构

### GNS3 Copilot 和 gns3-mcp 有什么区别？

两者都致力于将 AI 与 GNS3 结合，但采用的技术路径不同：

- **gns3-mcp**：基于 MCP (Model Context Protocol) 服务器，使用标准协议，互操作性更强
- **gns3-copilot**：基于 Streamlit + LangGraph，专注于多智能体工作流

### 为什么使用多智能体架构？

GNS3 Copilot 采用多智能体系统架构，包含以下角色：

- **规划智能体（Planning Agent）**：识别用户意图并制定详细任务计划
- **执行智能体（Execution Agent）**：根据计划逐步执行具体设备操作
- **监督智能体（Supervision Agent）**：持续监控和评估执行结果，发现问题时要求重试或通知专家智能体
- **专家智能体（Expert Agent）**：解决复杂问题，提供指导、纠正计划或提出解决方案

这种闭环结构确保可靠性和自我纠正能力。

### 为什么从 LangChain 迁移到 LangGraph？

最初使用 LangChain 和 ReAct 提示，但随着项目增长，遇到了以下问题：

- **上下文窗口膨胀**：导致"LLM 注意力不集中"和不可靠的工具选择
- **迭代限制**：LangChain/LangGraph 固有地具有 `recursion_limit` 和 `max_iterations` 约束

迁移到 LangGraph 后，实现了：
- 动态提示
- 层级多智能体工作流
- 适当的状态持久化
- 从架构层面解决上下文长度问题

### 为什么没有使用 MCP？

考虑过将工具包装为 MCP 代理以消除 UI 关注点，让任何 MCP 兼容客户端都能使用。但为了实验 LangGraph 的多智能体和 StateManager 功能，暂时搁置了这个想法，改用 Streamlit 构建 UI。

---

## 技术实现

### 为什么 fork gns3fy？

GNS3 Server API 最流行的 Python 客户端是 gns3fy，但它针对 GNS3 Server 2.2。该仓库已停止维护超过两年。

提交了一个小的 PR 以兼容新版 Pydantic，但没有收到响应。最终 fork 并扩展了该库。

基于 fork 的 gns3fy，构建了高级工具集合：
- 拓扑导出器
- 节点/链路创建
- 动态控制台端口查找
- 等等

所有工具都设计为接受和返回结构化的 JSON 对象和数组——这是与现代 LLM 配合最可靠的格式。

### 为什么使用 Nornir 而不是直接使用 Netmiko？

初始使用 Netmiko 直接配置设备。为了获得大规模并发能力，迁移到 Nornir + nornir-netmiko 插件。

**优势**：
- **Token 节省**：配置 5 个设备如果顺序执行需要至少 5 次 llm_calls，每次调用都携带之前的历史消息。使用 Nornir，所有 5 个设备的配置可以在单次工具调用中完成
- **时间效率**：逐个配置设备太慢。Nornir 可以同时配置多个设备
- **简化交互**：LLM 只需提供简单的 JSON 载荷（目标节点和命令列表）

### 如何处理多设备配置？

当设备（如 R-1）在 GNS3 中添加时，GNS3 Server 会分配控制台端口（如 5000）。

在 Qt 或 Web 界面中右键选择控制台打开配置窗口时，底层操作本质上是 `telnet [gns3server 地址] 5000`。

使用 Nornir 的 `nornir_netmiko` 插件可以：
1. 通过 GNS3 API 解析控制台端口
2. 生成并行的 Netmiko/telnet 会话
3. 同时执行命令
4. 返回结构化的 JSON 结果

### 为什么 JSON 格式对 LLM 重要？

JSON 格式确实难以阅读，但：
- 一旦在 UI（Streamlit）中渲染，仍然是可读的
- 现代化的 LLM 最擅长处理结构化数据
- 每个工具都有详细的类 docstring，LLM 依赖这些 docstring 来理解如何使用工具

提示技巧：为 LLM 提供几个示例，它倾向于按照示例进行操作。

---

## LLM 和提示工程

### 使用哪些 LLM 模型？

主要使用 **DeepSeek**，因为它：
- 非常实惠
- 模型能力满足需求

其他经验：
- **Gemini Flash**：便宜但功能有限
- **Grok Fast**：便宜但功能有限
- **MiniMax M2**：出乎意料地好
- **ChatGPT Network Engineer**：微调模型，在处理网络问题方面比通用模型更专业

通过 OpenRouter 注册只是为了验证 API 接口功能，结果在一两天内花了 $13 USD（约 ¥100 RMB）。

### 什么对代理性能影响最大？

**代理架构、提示和能力**比模型本身影响更大。

例如，Claude Code vs Warp（都使用 Sonnet 4.5）：
- Warp 更擅长处理 MCP 资源，但难以正确使用工具
- Claude Code 完全忽略资源，需要为它们编写包装器

### LLM 有时会产生错误的输出吗？

使用 LLM 就像打开一个盲盒... LLM 只是根据人类输入计算一个人类认为合理的输出。

一些有趣的测试案例：

**示例 1：子网掩码和反掩码的关系**
```
问题：子网掩码和反掩码（通配符掩码）是否 100% 满足和为 255 的关系？
即，如果子网掩码是 255.255.255.0，反掩码写为 0.0.0.255，
这个和为 255 的关系是否 100% 有效？
```

**示例 2：配置错误**
```
问题：为什么这个命令序列会抛出错误 'Bad mask /27 for address 192.168.10.10'？

R1#conf t 
R1(config)#int fa0/0 
R1(config-if)#ip add 192.168.10.10 255.255.255.224 
Bad mask /27 for address 192.168.10.10
```

---

## Human-in-the-Loop

### 如何实现人工干预？

当前概念：Human-in-the-Loop（人在环中）可以部分实现。但仍需要人工定义具体的操作或应该发生人工干预的点。

可能的实现方案：
- 添加一个按钮，允许人类在观察到出错时随时停止并干预
- 修改任务后恢复工作

目标：能够在不过度干扰的情况下跟随代理的动作——就像有人站在后面，实时看到他们的屏幕和动作，可以要求解释甚至更改某些东西。当前的代理还远未达到这个水平。

---

## 文档和知识

### 是否使用 RAG 与厂商文档集成？

这是网络工程师的竞争"护城河"。每个厂商都有自己的专有技术和专门文档。通用大语言模型无法涉足这个领域。

**挑战**：
- 如果要实现 RAG，需要精心组织和分块原始数据才能获得满意的结果，这代表了大量的工作
- 小众厂商的仿真器几乎无法从 LLM 获得有用帮助

**现状**：
- 对于学习，公开材料通常足够。LLM 的训练数据集自然不会遗漏网络巨头 Cisco 的相关文档
- 在中国，大多数人从华为、H3C、锐捷等厂商开始学习

**理想方案**：
- 每个设备厂商都启动"基于文档的知识服务（MCP）"——但这可能不现实
- 最现实的解决方案：集成搜索服务工具，如 Google Search API

### 如何管理设备凭证？

通过环境变量加载 Linux 用户名和密码。`linux_tools_nornir` 工具只需要关注命令列表和设备名称。

`src/gns3_copilot/ui_model/settings.py` 中的注释已列出了 .env 文件中包含的信息。

计划稍后添加更多环境变量字段。如果进行任何与安全相关的实验，将需要这些特定设备的用户名和密码。

---

## 拓扑管理

### 为什么只实现 CR（创建和读取）操作？

拓扑管理只实现 CRUD 的 CR（Create 和 Read）操作，因为不想让 LLM 破坏或修改已设置的拓扑。

### 为什么有设备启动工具但想要移除它？

`gns3_start_node.py` 工具可能需要被移除，因为：
- 处理问题时，LLM 有时会莫名其妙地假设设备未启动并执行该工具
- 无法验证设备是否真正启动
- 实现了内置的计时器等待功能：每个设备计划启动时间约 120 秒，每增加一个设备额外等待 20%

### 拓扑管理支持哪些设备？

`config_tools_nornir.py` 和 `display_tools_nornir.py` 接受 `platform` 和 `device_type` 作为工具参数。这允许利用 `nornir_netmiko` 支持的所有设备模型。

---

## 其他资源

### 相关文档

- [GNS3-Copilot Architecture](../Architecture/gns3_copilot_architecture.md)
- [Core Framework Detailed Design](../Architecture/Core%20Framework%20Detailed%20Design.md)

### 流程图

可以在 [Architecture](../Architecture/) 目录下查看流程图。Markdown 文档可能不完全准确或完整，因为它们是由 LLM 基于代码生成的。但 SVG 图像已经过修改，通常是正确的。

### 提示模板

主提示位于 `src/gns3_copilot/prompt/react_prompt.py`。

### 相关项目

- [gns3-mcp](https://github.com/ChistokhinSV/gns3-mcp) - 另一个 GNS3 + LLM 项目，基于 MCP 协议

---

## 参考资料和致谢

### 学习资源

- Powered by 《网络工程师的 Python 之路》
- Powered by 《网络工程师的 AI 之路》

### Streamlit 相关

- [Streamlit Widget Behavior](https://docs.streamlit.io/library/advanced-features/widget-behavior)
- Streamlit 官方文档关于 Widget 状态管理的说明
