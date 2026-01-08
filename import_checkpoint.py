from gns3_copilot.agent.checkpoint_utils import (
    import_checkpoint_from_file,
    list_thread_ids
)

from gns3_copilot.agent import langgraph_checkpointer

# 获取 checkpointer（直接使用实例，不要调用）
checkpointer = langgraph_checkpointer

# 导入前的线程列表
print("导入前的线程列表:")
thread_ids_before = list_thread_ids(checkpointer)
print(f"  {thread_ids_before}")

# 导入会话
file_path = "session_backup.json"

success, result = import_checkpoint_from_file(
    checkpointer=checkpointer,
    file_path=file_path
)

if success:
    print(f"✓ 会话已导入，新线程ID: {result}")
    
    # 导入后的线程列表
    print("\n导入后的线程列表:")
    thread_ids_after = list_thread_ids(checkpointer)
    print(f"  {thread_ids_after}")
    
    # 验证新线程
    print(f"\n验证新线程 {result}:")
    from gns3_copilot.agent import agent
    config = {"configurable": {"thread_id": result}}
    state = agent.get_state(config)
    print(f"  消息数量: {len(state.values.get('messages', []))}")
    if state.values.get('messages'):
        print(f"  第一条消息: {state.values['messages'][0]}")
else:
    print(f"✗ 导入失败: {result}")