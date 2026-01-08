from gns3_copilot.agent.checkpoint_utils import (
    export_checkpoint_to_file,
    list_thread_ids
)

from gns3_copilot.agent import langgraph_checkpointer

# 获取 checkpointer（直接使用实例，不要调用）
checkpointer = langgraph_checkpointer  # ✓ 正确：直接使用对象

# 列出所有线程
thread_ids = list_thread_ids(checkpointer)
print(f"可用的线程: {thread_ids}")

# 导出特定线程到文件
thread_id = "942a6a80-ba4a-4897-ac5f-1e8ab19e1af6"
file_path = "session_backup.json"

success = export_checkpoint_to_file(
    checkpointer=checkpointer,
    thread_id=thread_id,
    file_path=file_path
)

if success:
    print(f"✓ 会话已导出到: {file_path}")
else:
    print("✗ 导出失败")
