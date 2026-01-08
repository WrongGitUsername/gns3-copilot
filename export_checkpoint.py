"""
GNS3 Copilot Checkpoint Export Script

This script exports a checkpoint session from the SQLite database
to a JSON file. It allows you to backup sessions for migration
or archival purposes.

IMPORTANT: This script must be run from the project root directory:
    cd /path/to/gns3-copilot
    python export_checkpoint.py

Usage:
    1. First, run: python inspect_session.py to find available thread IDs
    2. Modify the thread_id variable below to the desired thread ID
    3. Modify the file_path variable if you want a different output file
    4. Run: python export_checkpoint.py
    5. The exported file will be saved in the project root directory

Features:
- Exports session data to JSON format
- Lists all available threads before export
- Provides clear success/failure feedback
- Exported files can be imported on other instances

Requirements:
- Must be run from project root directory
- Requires GNS3 Copilot to be properly installed
- Access to SQLite checkpoint database

Configuration:
    Modify these variables below to export a different session:
        thread_id = "your-thread-id-here"
        file_path = "your_backup_file.json"
"""

from gns3_copilot.agent.checkpoint_utils import (
    export_checkpoint_to_file,
    list_thread_ids
)

from gns3_copilot.agent import langgraph_checkpointer

# Get checkpointer (use instance directly, don't call)
checkpointer = langgraph_checkpointer  # ✓ Correct: use object directly

# List all threads
thread_ids = list_thread_ids(checkpointer)
print(f"Available threads: {thread_ids}")

# Export specific thread to file
thread_id = "942a6a80-ba4a-4897-ac5f-1e8ab19e1af6"
file_path = "session_backup.json"

success = export_checkpoint_to_file(
    checkpointer=checkpointer,
    thread_id=thread_id,
    file_path=file_path
)

if success:
    print(f"✓ Session exported to: {file_path}")
else:
    print("✗ Export failed")
