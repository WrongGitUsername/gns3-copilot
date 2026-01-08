"""
GNS3 Copilot Checkpoint Import Script

This script imports a checkpoint session from a JSON file into the
SQLite checkpoint database. It allows you to restore previously exported
sessions.

IMPORTANT: This script must be run from the project root directory:
    cd /path/to/gns3-copilot
    python import_checkpoint.py

Usage:
    1. Prepare your session_backup.json file in the project root
    2. Run: python import_checkpoint.py
    3. The script will display the thread ID of the imported session

Features:
- Imports session data from JSON file
- Creates a new thread ID for the imported session
- Displays thread lists before and after import
- Verifies the imported session by reading message count

Requirements:
- Must be run from project root directory
- session_backup.json must exist in the project root
- Requires GNS3 Copilot to be properly installed

Configuration:
    Modify the file_path variable below to import from a different file:
        file_path = "your_session_backup.json"
"""

from gns3_copilot.agent.checkpoint_utils import (
    import_checkpoint_from_file,
    list_thread_ids
)

from gns3_copilot.agent import langgraph_checkpointer

# Get checkpointer (use instance directly, don't call)
checkpointer = langgraph_checkpointer

# Thread list before import
print("Thread list before import:")
thread_ids_before = list_thread_ids(checkpointer)
print(f"  {thread_ids_before}")

# Import session
file_path = "session_backup.json"

success, result = import_checkpoint_from_file(
    checkpointer=checkpointer,
    file_path=file_path
)

if success:
    print(f"✓ Session imported, new thread ID: {result}")
    
    # Thread list after import
    print("\nThread list after import:")
    thread_ids_after = list_thread_ids(checkpointer)
    print(f"  {thread_ids_after}")
    
    # Verify new thread
    print(f"\nVerify new thread {result}:")
    from gns3_copilot.agent import agent
    config = {"configurable": {"thread_id": result}}
    state = agent.get_state(config)
    print(f"  Message count: {len(state.values.get('messages', []))}")
    if state.values.get('messages'):
        print(f"  First message: {state.values['messages'][0]}")
else:
    print(f"✗ Import failed: {result}")
