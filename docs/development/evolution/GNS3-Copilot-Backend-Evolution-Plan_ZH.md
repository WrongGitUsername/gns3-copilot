# 🏗️ GNS3-Copilot 后端演进计划

## 1. 架构愿景

从独立的 Streamlit 脚本过渡到**"双引擎"**架构。

* **引擎 A（遗留）**: Streamlit `app.py`，用于快速内部原型设计和调试。
* **引擎 B（现代）**: FastAPI `server.py`，作为 **BFF（Backend for Frontend）** 为现代 React UI 和移动端语音交互提供服务。

---

## 2. 核心技术策略

* **并发性**: 使用 FastAPI 的标准 `def` 路由，利用内部线程池处理同步 GNS3 API 调用和 LangGraph 执行。
* **配置**: 维持 `.env` 驱动的设置（本地优先）。凭据（LLM 密钥、GNS3 URL）通过环境变量加载；本地 MVP 不需要复杂的身份验证。
* **通信**: 实现 **SSE（Server-Sent Events）** 用于实时 AI "打字"效果和工具调用状态更新。
* **语音集成**: 实现"中继"模式：`浏览器麦克风 -> FastAPI -> 商业 STT (Whisper) -> LangGraph -> 商业 TTS -> 浏览器扬声器`。

---

## 3. 实施路线图

### 第一阶段：API 基础设施（基础）

* **目标**: 建立 FastAPI 项目结构并启用跨源通信。
* **任务**:
1. 安装 `fastapi` 和 `uvicorn`。
2. 创建 `api/main.py` 并配置 **CORS** 中间件（对 React 至关重要）。
3. 为可扩展性设置路由器目录结构。

### 第二阶段：LangGraph 集成（"大脑"）

* **目标**: 将 LangGraph 智能体暴露为统一的流式 API。
* **任务**:
1. 开发 `POST /agent/stream` 端点。
2. 使用 `asyncio.to_thread` 或事件泵队列包装同步 `graph.stream`。
3. 定义标准 SSE 消息模式（例如，`type: text` 用于内容，`type: tool` 用于操作状态）。

### 第三阶段：语音交互管道

* **目标**: 使用商业 API 启用语音到命令功能。
* **任务**:
1. 创建 `POST /agent/voice-chat` 以接收音频文件（`.webm`/`.wav`）。
2. 集成 **OpenAI Whisper API** 进行 STT（语音转文本）。
3. 将转录的文本连接到现有的 LangGraph 逻辑，并可选择通过 TTS 返回音频。

### 第四阶段：项目和拓扑服务

* **目标**: 为前端提供 GNS3 项目元数据。
* **任务**:
1. 实现 `GET /projects` 列出可用的 GNS3 拓扑。
2. 实现 `GET /projects/{id}/topology` 以获取 React Flow 可视化数据。

---

## 4. 推荐的项目结构

```text
src/gns3_copilot/
├── api/
│   ├── __init__.py
│   ├── main.py              # 入口点 & 中间件配置
│   ├── dependencies.py      # 共享逻辑（Context/配置）
│   └── routers/
│       ├── __init__.py
│       ├── agent.py         # 聊天、流式和语音端点
│       └── projects.py      # 项目和拓扑管理
├── tools/                   # 现有同步 GNS3 工具（未更改）
├── agent/                   # 现有 LangGraph 逻辑（未更改）
└── .env                     # 本地 API 密钥 & GNS3 服务器配置

```

---

## 5. 当前冲刺清单

* [ ] **设置**: 运行 `pip install fastapi uvicorn pydantic-settings`。
* [ ] **脚手架**: 创建 `api/` 目录并初始化 `main.py`。
* [ ] **核心 API**: 实现 `/agent/stream` 端点并通过 Swagger UI (`/docs`) 验证。
* [ ] **测试**: 确保 API 正确读取 `.env` 变量而无需手动注入。
