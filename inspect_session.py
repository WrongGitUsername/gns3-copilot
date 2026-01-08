"""
GNS3 Copilot Session Inspector

This script provides a command-line interface for inspecting LangGraph
checkpoint sessions. It displays detailed information about session state,
message statistics, and UI compatibility.

IMPORTANT: This script must be run from the project root directory:
    cd /path/to/gns3-copilot
    python inspect_session.py

Usage:
    python inspect_session.py

Features:
- List all available thread IDs
- Inspect specific thread details
- Validate UI compatibility
- Display message previews

Requirements:
- Must be run from project root directory
- Requires GNS3 Copilot to be properly installed
- Access to SQLite checkpoint database
"""

import json
from gns3_copilot.agent.checkpoint_utils import (
    inspect_session,
    list_thread_ids,
)
from gns3_copilot.agent import agent, langgraph_checkpointer


def print_separator(char="=", length=60):
    """Print a separator line."""
    print(char * length)


def print_thread_info(thread_id: str, info: dict, verbose: bool = False):
    """
    Print detailed information about a thread.

    Args:
        thread_id: Thread ID to display
        info: Session information from inspect_session()
        verbose: Whether to show verbose output
    """
    print(f"\n{'='*60}")
    print(f"Thread ID: {thread_id}")
    print(f"{'='*60}")
    
    # Error handling
    if "error" in info:
        print(f"\n❌ Error: {info['error']}")
        return
    
    # Basic information
    print(f"\n📊 Message Count: {info['message_count']}")
    print(f"   - Human: {info['message_types']['human']}")
    print(f"   - AI: {info['message_types']['ai']}")
    print(f"   - Tool: {info['message_types']['tool']}")
    print(f"   - Unknown: {info['message_types']['unknown']}")
    
    print(f"\n🔄 Next Action: {info['next']}")
    print(f"📍 Step: {info['step']}")
    print(f"⏳ Pending Tasks: {info['pending_tasks']}")
    print(f"⚠️  Has Interrupts: {info['has_interrupts']}")
    
    # Conversation info
    if info['conversation_title']:
        print(f"\n💬 Conversation Title: {info['conversation_title']}")
    
    if info['selected_project']:
        project = info['selected_project']
        if isinstance(project, tuple) and len(project) >= 5:
            print(f"\n🏗️  Selected Project:")
            print(f"   - Name: {project[0]}")
            print(f"   - ID: {project[1]}")
            print(f"   - Devices: {project[2]}")
            print(f"   - Links: {project[3]}")
            print(f"   - Status: {project[4]}")
        else:
            print(f"\n🏗️  Selected Project: {project}")
    
    # UI compatibility
    print(f"\n✅ UI Compatible: {info['ui_compatible']}")
    if not info['ui_compatible']:
        print(f"❌ Validation Error: {info['validation_error']}")
    
    # Latest message
    if info['latest_message']:
        print(f"\n📝 Latest Message:")
        print(f"   {info['latest_message'][:100]}{'...' if len(info['latest_message']) > 100 else ''}")
    
    # Verbose output
    if verbose and 'messages_preview' in info:
        print(f"\n📋 Message Preview:")
        for msg in info['messages_preview'][:10]:  # Show first 10 messages
            print(f"\n   [{msg['index']}] {msg['type']}")
            if 'content' in msg:
                print(f"   Content: {msg['content']}")
            if 'tool_calls_count' in msg:
                print(f"   Tool Calls: {msg['tool_calls_count']}")
        
        if len(info['messages_preview']) > 10:
            print(f"\n   ... and {len(info['messages_preview']) - 10} more messages")


def main():
    """Main function for session inspection."""
    print_separator()
    print("GNS3 Copilot - Session Inspector")
    print_separator()
    
    # List all available threads
    print("\n📚 Available Threads:")
    thread_ids = list_thread_ids(langgraph_checkpointer)
    
    if not thread_ids:
        print("   No threads found in checkpoint database.")
        return
    
    for idx, thread_id in enumerate(thread_ids, 1):
        # Get basic info for each thread
        info = inspect_session(thread_id, agent, verbose=False)
        title = info.get('conversation_title', 'Untitled')
        msg_count = info.get('message_count', 0)
        
        print(f"\n   {idx}. {thread_id}")
        print(f"      Title: {title}")
        print(f"      Messages: {msg_count}")
    
    # Ask user to select a thread
    print(f"\n{'='*60}")
    selection = input(
        "\nEnter thread number to inspect (or 'all' to inspect all, 'q' to quit): "
    ).strip()
    
    if selection.lower() == 'q':
        print("\n👋 Goodbye!")
        return
    
    if selection.lower() == 'all':
        # Inspect all threads
        verbose_input = input("\nShow verbose output? (y/n): ").strip().lower()
        verbose = verbose_input == 'y'
        
        for thread_id in thread_ids:
            info = inspect_session(thread_id, agent, verbose=verbose)
            print_thread_info(thread_id, info, verbose=verbose)
    else:
        # Inspect specific thread
        try:
            idx = int(selection) - 1
            if 0 <= idx < len(thread_ids):
                thread_id = thread_ids[idx]
                
                verbose_input = input("\nShow verbose output? (y/n): ").strip().lower()
                verbose = verbose_input == 'y'
                
                info = inspect_session(thread_id, agent, verbose=verbose)
                print_thread_info(thread_id, info, verbose=verbose)
            else:
                print(f"\n❌ Invalid selection. Please enter a number between 1 and {len(thread_ids)}.")
        except ValueError:
            print("\n❌ Invalid input. Please enter a number.")
    
    print(f"\n{'='*60}")
    print("✅ Inspection complete!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()