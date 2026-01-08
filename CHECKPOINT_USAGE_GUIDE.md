# Checkpoint 导出和导入使用指南

## 概述

`export_checkpoint.py` 和 `import_checkpoint.py` 用于导出和导入 GNS3 Copilot 的会话数据（checkpoint），实现会话备份和迁移功能。

---

## 文件说明

### 1. export_checkpoint.py
导出指定线程的会话数据到 JSON 文件。

### 2. import_checkpoint.py
从 JSON 文件导入会话数据到新的线程。

---

## 使用步骤

### 导出会话

1. **确认会话存在**
   - 确保 GNS3 Copilot 应用已经运行过，并且有对话会话
   - 会话数据存储在 `gns3_langgraph.db` 数据库中

2. **修改 export_checkpoint.py**
   ```python
   # 脚本会自动列出所有可用的线程 ID
   # 找到您想要导出的线程 ID
   
   # 修改 thread_id 为实际的线程 ID
   thread_id = "your-actual-thread-id-here"
   
   # 修改输出文件名（可选）
   file_path = "session_backup.json"
   ```

3. **运行导出脚本**
   ```bash
   python export_checkpoint.py
   ```

4. **检查输出**
   - 成功时会显示：`✓ 会话已导出到: session_backup.json`
   - 导出的文件包含完整的会话数据，包括：
     - 消息历史（用户消息、AI 响应、工具调用）
     - 会话标题
     - 配置信息
     - 元数据

### 导入会话

1. **确保导出文件存在**
   - 确认 `session_backup.json` 文件存在且格式正确

2. **运行导入脚本**
   ```bash
   python import_checkpoint.py
   ```

3. **检查输出**
   - 成功时会显示：
     ```
     ✓ 会话已导入，新线程ID: 99488600-f851-475c-a668-e9fdfcca7273
     导入后的线程列表:
       ['99488600-f851-475c-a668-e9fdfcca7273', 'efb5ad1c-22bc-4c8a-a6d5-12556c00a3a5']
     验证新线程 99488600-f851-475c-a668-e9fdfcca7273:
       消息数量: 27
       第一条消息: content='检查设备配置.' additional_kwargs={} response_metadata={}
     ```

4. **在 GNS3 Copilot 中访问**
   - 重启 GNS3 Copilot 应用
   - 新导入的会话将显示在会话列表中
   - 可以继续在导入的会话中进行对话

---

## 高级用法

### 列出所有线程

```python
from gns3_copilot.agent.checkpoint_utils import list_thread_ids
from gns3_copilot.agent import langgraph_checkpointer

checkpointer = langgraph_checkpointer
thread_ids = list_thread_ids(checkpointer)
print(f"可用的线程: {thread_ids}")
```

### 导入时指定线程 ID

```python
from gns3_copilot.agent.checkpoint_utils import import_checkpoint_from_file
from gns3_copilot.agent import langgraph_checkpointer

checkpointer = langgraph_checkpointer
file_path = "session_backup.json"

# 使用自定义线程 ID
custom_thread_id = "my-custom-thread-id"
success, result = import_checkpoint_from_file(
    checkpointer=checkpointer,
    file_path=file_path,
    new_thread_id=custom_thread_id
)
```

### 批量导出

```python
from gns3_copilot.agent.checkpoint_utils import list_thread_ids, export_checkpoint_to_file
from gns3_copilot.agent import langgraph_checkpointer

checkpointer = langgraph_checkpointer
thread_ids = list_thread_ids(checkpointer)

for i, thread_id in enumerate(thread_ids, 1):
    file_path = f"session_backup_{i}.json"
    success = export_checkpoint_to_file(
        checkpointer=checkpointer,
        thread_id=thread_id,
        file_path=file_path
    )
    if success:
        print(f"✓ 会话 {i} 已导出到: {file_path}")
```

---

## 导出文件格式

导出的 JSON 文件包含以下结构：

```json
{
  "checkpoint": {
    "v": 1,
    "ts": "2026-01-08T14:59:05.445123",
    "id": "checkpoint-id",
    "channel_values": {
      "messages": [
        {
          "type": "human",
          "content": "用户消息内容",
          "additional_kwargs": {},
          "response_metadata": {}
        },
        {
          "type": "ai",
          "content": "AI 响应内容",
          "tool_calls": [],
          "additional_kwargs": {},
          "response_metadata": {}
        }
      ],
      "conversation_title": "会话标题",
      "llm_calls": 5
    },
    "channel_versions": {
      "messages": 27
    }
  },
  "config": {
    "configurable": {
      "thread_id": "original-thread-id",
      "checkpoint_ns": ""
    }
  },
  "metadata": {
    "source": "export"
  }
}
```

---

## 消息类型说明

导出的消息包含以下类型：

- **human**: 用户消息（HumanMessage）
- **ai**: AI 响应（AIMessage）
- **tool**: 工具调用结果（ToolMessage）

---

## 常见问题

### Q1: 导出时提示 "Checkpoint not found for thread_id"
**A**: 线程 ID 不正确。运行 `python export_checkpoint.py` 查看所有可用的线程 ID，然后使用正确的 ID。

### Q2: 导入时提示 "Invalid JSON format in file"
**A**: 导出的 JSON 文件格式不正确或已损坏。请重新导出会话数据。

### Q3: 导入的会话在 GNS3 Copilot 中看不到
**A**: 重启 GNS3 Copilot 应用，新导入的会话会显示在会话列表中。

### Q4: 导入的消息显示为字符串而不是消息对象
**A**: 这是正常现象。消息在数据库中存储为 LangChain 消息对象，在 UI 中会正确显示。

---

## 技术细节

### 消息序列化
- 导出时，消息会被序列化为 JSON 兼容的字典格式
- 消息类型（human/ai/tool）会被保留
- 消息内容、工具调用、元数据等都会被完整保存

### 消息反序列化
- 导入时，字典格式的消息会被反序列化为 LangChain 消息对象
- 支持的消息类型：HumanMessage、AIMessage、ToolMessage
- 自动从字符串格式解析消息类型和内容

### 检查点验证
- 导入前会验证数据结构的完整性
- 检查必需的字段是否存在
- 确保数据格式符合 LangGraph 要求

---

## 注意事项

1. **数据库锁定**
   - 不要在 GNS3 Copilot 运行时手动修改 `gns3_langgraph.db` 文件
   - 建议在 GNS3 Copilot 未运行时进行导出和导入操作

2. **线程 ID 唯一性**
   - 每次导入会创建新的线程 ID
   - 可以使用自定义线程 ID，但必须确保唯一性

3. **数据备份**
   - 导出前建议备份 `gns3_langgraph.db` 文件
   - 导出的 JSON 文件可以作为备份保存

4. **跨环境迁移**
   - 导出的 JSON 文件可以用于不同环境之间的会话迁移
   - 确保目标环境使用相同版本的 GNS3 Copilot

---

## 示例工作流程

### 备份所有会话

```bash
# 1. 导出所有会话
python export_all_sessions.py

# 2. 将导出的文件备份到安全位置
cp session_backup_*.json /backup/location/

# 3. （可选）清理旧会话
# 可以手动删除不需要的会话
```

### 迁移会话到新环境

```bash
# 1. 在旧环境导出会话
python export_checkpoint.py

# 2. 将导出的文件复制到新环境
cp session_backup.json /new/environment/

# 3. 在新环境导入会话
python import_checkpoint.py

# 4. 重启 GNS3 Copilot
streamlit run src/gns3_copilot/main.py
```

---

## 相关文件

- `src/gns3_copilot/agent/checkpoint_utils.py` - 检查点工具函数
- `src/gns3_copilot/agent/gns3_copilot.py` - LangGraph 代理实现
- `gns3_langgraph.db` - 检查点数据库

---

## 更新日志

- 2026-01-08: 完善消息序列化和反序列化功能，支持从字符串格式解析消息
- 2026-01-08: 添加完整的 config 和 metadata 支持
- 2026-01-08: 初始版本，支持基本的导出和导入功能