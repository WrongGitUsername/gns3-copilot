# GNS3 Copilot Checkpoint Debugging Guide

本指南提供了 LangGraph checkpoint 调试、导出和导入的完整说明。

## 目录

1. [概述](#概述)
2. [核心概念](#核心概念)
3. [Checkpoint Utils API](#checkpoint-utils-api)
4. [调试工具](#调试工具)
5. [导出和导入 Checkpoint](#导出和导入-checkpoint)
6. [消息序列化](#消息序列化)
7. [UI 兼容性验证](#ui-兼容性验证)
8. [使用示例](#使用示例)
9. [故障排除](#故障排除)

## 概述

GNS3 Copilot 使用 LangGraph 的 checkpointer 机制来持久化对话状态。`checkpoint_utils.py` 模块提供了用于管理 checkpoint 的实用工具。

### 核心功能

- **Thread ID 管理**: 列出和管理所有对话线程
- **Checkpoint 导出**: 将 checkpoint 导出到 JSON 文件
- **Checkpoint 导入**: 从 JSON 文件恢复 checkpoint
- **会话检查**: 查看和分析会话状态
- **消息验证**: 验证消息的 UI 兼容性

## 核心概念

### Checkpoint 结构

Checkpoint 包含以下主要组件：

```python
{
    "checkpoint": {
        "v": 3,                    # 版本号
        "ts": "timestamp",           # 时间戳
        "id": "checkpoint-id",        # Checkpoint ID
        "channel_values": {
            "messages": [...],          # 消息列表
            "conversation_title": "...", # 对话标题
            "selected_project": (...),   # 选中的项目
        },
        "channel_versions": {...},      # 通道版本
        "versions_seen": {...},         # 已见版本
        "next": None                 # 下一步动作
    },
    "config": {...},                # 配置信息
    "metadata": {...}               # 元数据
}
```

### 消息类型

- **HumanMessage**: 用户输入的消息
- **AIMessage**: AI 响应的消息，可能包含 tool_calls
- **ToolMessage**: 工具执行结果

## Checkpoint Utils API

### `list_thread_ids(checkpointer)`

列出所有唯一的 thread ID，按最近活动排序。

**参数:**
- `checkpointer`: LangGraph checkpointer 实例

**返回:**
- `list[str]`: thread ID 列表，按最近活动降序排列

**示例:**
```python
from gns3_copilot.agent.checkpoint_utils import list_thread_ids
from gns3_copilot.agent import langgraph_checkpointer

threads = list_thread_ids(langgraph_checkpointer)
for thread_id in threads:
    print(f"Thread: {thread_id}")
```

### `generate_thread_id()`

生成一个新的唯一 thread ID。

**返回:**
- `str`: UUID 格式的 thread ID

**示例:**
```python
from gns3_copilot.agent.checkpoint_utils import generate_thread_id

new_thread_id = generate_thread_id()
print(f"New thread ID: {new_thread_id}")
```

### `validate_checkpoint_data(data)`

验证 checkpoint 数据结构。

**参数:**
- `data`: 要验证的 checkpoint 数据字典

**返回:**
- `tuple[bool, str]`: (是否有效, 错误消息)

**示例:**
```python
from gns3_copilot.agent.checkpoint_utils import validate_checkpoint_data

is_valid, error_msg = validate_checkpoint_data(checkpoint_data)
if not is_valid:
    print(f"Invalid checkpoint: {error_msg}")
```

### `serialize_message(msg)`

将 LangChain 消息序列化为 JSON 兼容格式。

**参数:**
- `msg`: LangChain 消息对象

**返回:**
- `dict`: 序列化的消息

**示例:**
```python
from gns3_copilot.agent.checkpoint_utils import serialize_message
from langchain.messages import AIMessage

msg = AIMessage(content="Hello!", tool_calls=[...])
serialized = serialize_message(msg)
# {"type": "ai", "content": "Hello!", "tool_calls": [...]}
```

### `deserialize_message(msg_dict)`

将字典反序列化为 LangChain 消息对象。

**参数:**
- `msg_dict`: 序列化的消息字典

**返回:**
- `Message`: LangChain 消息对象

**示例:**
```python
from gns3_copilot.agent.checkpoint_utils import deserialize_message

msg_dict = {"type": "ai", "content": "Hello!", "tool_calls": [...]}
msg = deserialize_message(msg_dict)
# AIMessage(content="Hello!", tool_calls=[...])
```

### `validate_messages_for_ui(messages)`

验证消息列表的 UI 兼容性。

**参数:**
- `messages`: 消息对象列表

**返回:**
- `tuple[bool, str, list[str]]`: (是否有效, 错误消息, 错误列表)

**示例:**
```python
from gns3_copilot.agent.checkpoint_utils import validate_messages_for_ui

is_valid, error_msg, errors = validate_messages_for_ui(messages)
if not is_valid:
    print(f"Validation failed: {error_msg}")
    for err in errors:
        print(f"  - {err}")
```

### `inspect_session(thread_id, graph, verbose=False)`

检查会话状态，返回人类可读的信息。

**参数:**
- `thread_id`: 要检查的 thread ID
- `graph`: 编译的 LangGraph agent 实例
- `verbose`: 是否包含详细的消息预览

**返回:**
- `dict`: 包含会话信息的字典

**示例:**
```python
from gns3_copilot.agent.checkpoint_utils import inspect_session
from gns3_copilot.agent import agent

info = inspect_session(thread_id, agent, verbose=True)
print(f"Messages: {info['message_count']}")
print(f"UI Compatible: {info['ui_compatible']}")
print(f"Latest Message: {info['latest_message']}")
```

### `export_checkpoint_to_file(checkpointer, thread_id, file_path)`

将 checkpoint 导出到文件。

**参数:**
- `checkpointer`: LangGraph checkpointer 实例
- `thread_id`: 要导出的 thread ID
- `file_path`: 输出文件路径

**返回:**
- `bool`: 是否成功

**示例:**
```python
from gns3_copilot.agent.checkpoint_utils import export_checkpoint_to_file
from gns3_copilot.agent import langgraph_checkpointer

success = export_checkpoint_to_file(
    langgraph_checkpointer,
    "thread-id-123",
    "checkpoint_backup.txt"
)
if success:
    print("Checkpoint exported successfully!")
```

### `import_checkpoint_from_file(checkpointer, file_path, new_thread_id=None)`

从文件导入 checkpoint。

**参数:**
- `checkpointer`: LangGraph checkpointer 实例
- `file_path`: 输入文件路径
- `new_thread_id`: 可选的新 thread ID，如果不提供则自动生成

**返回:**
- `tuple[bool, str]`: (是否成功, 新 thread ID 或错误消息)

**示例:**
```python
from gns3_copilot.agent.checkpoint_utils import import_checkpoint_from_file
from gns3_copilot.agent import langgraph_checkpointer

success, result = import_checkpoint_from_file(
    langgraph_checkpointer,
    "checkpoint_backup.txt"
)
if success:
    print(f"Imported to thread: {result}")
else:
    print(f"Import failed: {result}")
```

## 调试工具

### `inspect_session.py` 脚本

提供交互式命令行界面用于检查会话。

**使用方法:**
```bash
python inspect_session.py
```

**功能:**
- 列出所有可用的 thread ID
- 检查特定 thread 的详细信息
- 显示消息统计和类型分布
- 验证 UI 兼容性
- 显示消息预览（verbose 模式）

**示例输出:**
```
==============================================================
GNS3 Copilot - Session Inspector
==============================================================

📚 Available Threads:

   1. 550e8400-e29b-41d4-a716-446655440000
      Title: Network Configuration
      Messages: 5

==============================================================

Enter thread number to inspect (or 'all' to inspect all, 'q' to quit): 1

==============================================================
Thread ID: 550e8400-e29b-41d4-a716-446655440000
==============================================================

📊 Message Count: 5
   - Human: 2
   - AI: 2
   - Tool: 1

🔄 Next Action: None
📍 Step: 5
⏳ Pending Tasks: 0
⚠️  Has Interrupts: False

💬 Conversation Title: Network Configuration
✅ UI Compatible: True
```

## 导出和导入 Checkpoint

### 导出 Checkpoint

使用 `export_checkpoint.py` 或 API 函数：

```python
from gns3_copilot.agent.checkpoint_utils import export_checkpoint_to_file

# 导出指定 thread
success = export_checkpoint_to_file(
    langgraph_checkpointer,
    "thread-id",
    "backup.txt"
)
```

导出的文件包含：
- 完整的 checkpoint 数据
- 消息（已序列化为 JSON）
- 配置信息
- 元数据

### 导入 Checkpoint

使用 `import_checkpoint.py` 或 API 函数：

```python
from gns3_copilot.agent.checkpoint_utils import import_checkpoint_from_file

# 导入到新 thread
success, new_thread_id = import_checkpoint_from_file(
    langgraph_checkpointer,
    "backup.txt"
)

# 导入到指定 thread
success, new_thread_id = import_checkpoint_from_file(
    langgraph_checkpointer,
    "backup.txt",
    "custom-thread-id"
)
```

## 消息序列化

### 为什么需要序列化

LangChain 消息对象包含复杂的数据结构，不能直接序列化为 JSON。序列化确保：

1. **JSON 兼容性**: 可以安全地保存到文件
2. **跨实例迁移**: 可以在不同实例之间迁移
3. **UI 兼容性**: 确保导入的消息可以被 UI 正确渲染

### 序列化过程

```python
# 原始消息
msg = AIMessage(
    content="I'll help you",
    tool_calls=[
        ToolCall(id="call-1", name="tool", args={"param": "value"})
    ]
)

# 序列化
serialized = serialize_message(msg)
# {
#     "type": "ai",
#     "content": "I'll help you",
#     "tool_calls": [
#         {"id": "call-1", "name": "tool", "args": {"param": "value"}, "type": "tool_call"}
#     ],
#     "additional_kwargs": {},
#     "response_metadata": {},
#     "id": msg.id
# }
```

### 反序列化过程

```python
# 序列化的数据
msg_dict = {
    "type": "ai",
    "content": "I'll help you",
    "tool_calls": [...]
}

# 反序列化
msg = deserialize_message(msg_dict)
# AIMessage(content="I'll help you", tool_calls=[...])
```

## UI 兼容性验证

### 验证规则

`validate_messages_for_ui` 函数检查以下规则：

1. **HumanMessage**
   - 必须有 `content` 字段

2. **AIMessage**
   - 必须有 `content` 字段
   - 如果有 `tool_calls`，每个 tool call 必须有：
     - `id`: 工具调用 ID
     - `name`: 工具名称
     - `args`: 工具参数

3. **ToolMessage**
   - 必须有 `content` 字段
   - 必须有非空的 `tool_call_id`
   - 必须有非空的 `name`

### 使用验证

```python
from gns3_copilot.agent.checkpoint_utils import validate_messages_for_ui

# 验证消息列表
is_valid, error_msg, errors = validate_messages_for_ui(messages)

if not is_valid:
    print("⚠️  Messages are not UI compatible!")
    print(f"Error: {error_msg}")
    for error in errors:
        print(f"  - {error}")
else:
    print("✅ Messages are UI compatible")
```

## 使用示例

### 示例 1: 备份和恢复会话

```python
from gns3_copilot.agent.checkpoint_utils import (
    export_checkpoint_to_file,
    import_checkpoint_from_file,
    list_thread_ids
)

# 列出所有 thread
threads = list_thread_ids(checkpointer)
print(f"Found {len(threads)} threads")

# 导出第一个 thread
if threads:
    thread_id = threads[0]
    backup_file = f"backup_{thread_id}.txt"
    
    success = export_checkpoint_to_file(
        checkpointer, thread_id, backup_file
    )
    
    if success:
        print(f"✅ Exported to {backup_file}")
        
        # 恢复到新 thread
        success, new_thread = import_checkpoint_from_file(
            checkpointer, backup_file
        )
        
        if success:
            print(f"✅ Restored to {new_thread}")
```

### 示例 2: 检查会话状态

```python
from gns3_copilot.agent.checkpoint_utils import (
    inspect_session,
    list_thread_ids
)
from gns3_copilot.agent import agent

# 获取所有 thread
threads = list_thread_ids(checkpointer)

# 检查每个 thread
for thread_id in threads:
    info = inspect_session(thread_id, agent, verbose=False)
    
    print(f"\nThread: {thread_id}")
    print(f"  Title: {info.get('conversation_title', 'Untitled')}")
    print(f"  Messages: {info['message_count']}")
    print(f"  UI Compatible: {info['ui_compatible']}")
    
    if not info['ui_compatible']:
        print(f"  ❌ Error: {info['validation_error']}")
```

### 示例 3: 验证消息

```python
from gns3_copilot.agent.checkpoint_utils import (
    serialize_message,
    deserialize_message,
    validate_messages_for_ui
)
from langchain.messages import AIMessage

# 创建消息
msg = AIMessage(
    content="I'll use tools",
    tool_calls=[
        ToolCall(id="call-1", name="tool", args={"param": "value"})
    ]
)

# 序列化
serialized = serialize_message(msg)
print(f"Serialized: {serialized}")

# 反序列化
restored = deserialize_message(serialized)
print(f"Restored: {restored}")

# 验证
is_valid, error_msg, errors = validate_messages_for_ui([restored])
print(f"Valid: {is_valid}")
if not is_valid:
    print(f"Error: {error_msg}")
```

## 故障排除

### 问题: 导入后消息无法显示

**症状**: 导入 checkpoint 后，UI 无法显示消息。

**解决方案**:
1. 使用 `inspect_session` 检查 UI 兼容性：
```python
info = inspect_session(thread_id, agent)
print(f"UI Compatible: {info['ui_compatible']}")
if not info['ui_compatible']:
    print(f"Errors: {info['validation_errors']}")
```

2. 检查消息序列化：
```python
from gns3_copilot.agent.checkpoint_utils import validate_messages_for_ui
is_valid, _, errors = validate_messages_for_ui(messages)
for error in errors:
    print(error)
```

### 问题: tool_calls 丢失

**症状**: 导入后 AIMessage 的 tool_calls 为空。

**原因**: 序列化时 tool_calls 结构不完整。

**解决方案**: 确保 tool_calls 包含所有必需字段：
```python
tool_calls = [
    {
        "id": "call-1",        # 必需
        "name": "tool_name",    # 必需
        "args": {"param": ...},  # 必需
        "type": "tool_call"      # 推荐
    }
]
```

### 问题: 中文内容乱码

**症状**: 导出的文件中中文显示为乱码。

**原因**: 文件编码问题。

**解决方案**: 确保使用 UTF-8 编码：
```python
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

### 问题: 导入失败

**症状**: `import_checkpoint_from_file` 返回错误。

**常见原因和解决方案**:

1. **文件不存在**: 检查文件路径
```python
import os
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
```

2. **JSON 格式错误**: 验证 JSON 格式
```python
import json
try:
    with open(file_path, "r") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"Invalid JSON: {e}")
```

3. **缺少必需字段**: 验证 checkpoint 数据
```python
from gns3_copilot.agent.checkpoint_utils import validate_checkpoint_data
is_valid, error_msg = validate_checkpoint_data(data)
if not is_valid:
    print(f"Invalid data: {error_msg}")
```

### 问题: 检查失败

**症状**: `checkpointer.get_tuple()` 返回 None。

**解决方案**:
1. 验证 thread ID 存在：
```python
threads = list_thread_ids(checkpointer)
if thread_id not in threads:
    print(f"Thread not found: {thread_id}")
```

2. 检查 checkpointer 连接：
```python
if not hasattr(checkpointer, 'conn'):
    print("Checkpointer has no connection")
```

## 最佳实践

1. **定期备份**: 定期导出重要会话作为备份
2. **验证导入**: 导入后使用 `inspect_session` 验证
3. **使用 inspect_session**: 在调试和检查会话时使用
4. **保持 UTF-8 编码**: 导出和导入时使用 UTF-8 编码
5. **验证 UI 兼容性**: 导入前验证消息兼容性

## 相关文档

- [Checkpoint Usage Guide](../CHECKPOINT_USAGE_GUIDE.md)
- [API Reference](../README.md)
- [Architecture Design](../architecture/core-framework-design.md)