"""
Reading page for GNS3 Copilot application.

This module provides a reading interface with Calibre ebook viewer and
a multi-note management system for taking and organizing reading notes.

Features:
- Calibre ebook viewer embedded in iframe
- Multi-note management system (create, select, delete notes)
- Notes saved as Markdown files
- Download notes functionality
- Automatic notes directory creation
"""

import os
from datetime import datetime
from typing import Any

import streamlit as st

from gns3_copilot.log_config import setup_logger

logger = setup_logger("reading")

# Initialize session state for note management
if "current_note_filename" not in st.session_state:
    st.session_state.current_note_filename = None

if "current_note_content" not in st.session_state:
    st.session_state.current_note_content = ""

if "new_note_name" not in st.session_state:
    st.session_state.new_note_name = ""


def get_notes_directory() -> str:
    """Get the notes directory path from session state or default."""
    notes_dir = st.session_state.get("READING_NOTES_DIR", "notes")
    # Make it absolute path relative to current working directory
    if not os.path.isabs(notes_dir):
        notes_dir = os.path.join(os.getcwd(), notes_dir)
    return notes_dir


def ensure_notes_directory() -> str:
    """Ensure the notes directory exists, create if not."""
    notes_dir = get_notes_directory()
    if not os.path.exists(notes_dir):
        try:
            os.makedirs(notes_dir)
            logger.info("Created notes directory: %s", notes_dir)
        except Exception as e:
            logger.error("Failed to create notes directory: %s", e)
            st.error(f"Failed to create notes directory: {e}")
    return notes_dir


def list_note_files() -> list[str]:
    """List all markdown note files in the notes directory."""
    notes_dir = ensure_notes_directory()
    note_files = []
    try:
        for filename in os.listdir(notes_dir):
            if filename.endswith(".md"):
                note_files.append(filename)
        note_files.sort()  # Sort alphabetically
    except Exception as e:
        logger.error("Failed to list note files: %s", e)
    return note_files


def load_note_content(filename: str) -> str:
    """Load note content from file."""
    notes_dir = ensure_notes_directory()
    filepath = os.path.join(notes_dir, filename)
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        logger.debug("Loaded note: %s", filename)
        return content
    except Exception as e:
        logger.error("Failed to load note %s: %s", filename, e)
        return ""


def save_note_content(filename: str, content: str) -> bool:
    """Save note content to file."""
    notes_dir = ensure_notes_directory()
    filepath = os.path.join(notes_dir, filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info("Saved note: %s", filename)
        return True
    except Exception as e:
        logger.error("Failed to save note %s: %s", filename, e)
        return False


def delete_note_file(filename: str) -> bool:
    """Delete a note file."""
    notes_dir = ensure_notes_directory()
    filepath = os.path.join(notes_dir, filename)
    try:
        os.remove(filepath)
        logger.info("Deleted note: %s", filename)
        return True
    except Exception as e:
        logger.error("Failed to delete note %s: %s", filename, e)
        return False


def create_new_note() -> str | None:
    """Create a new note file."""
    note_name = st.session_state.get("new_note_name", "").strip()
    if not note_name:
        st.error("Please enter a note name.")
        return None

    # Ensure filename ends with .md
    if not note_name.endswith(".md"):
        note_name += ".md"

    # Sanitize filename (remove invalid characters)
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        note_name = note_name.replace(char, "_")

    notes_dir = ensure_notes_directory()
    filepath = os.path.join(notes_dir, note_name)

    # Check if file already exists
    if os.path.exists(filepath):
        st.error(f"Note '{note_name}' already exists.")
        return None

    # Create empty note with header
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        initial_content = f"# {note_name[:-3]}\n\nCreated: {timestamp}\n\n"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(initial_content)
        logger.info("Created new note: %s", note_name)
        # Clear the input field after successful creation
        st.session_state.new_note_name = ""
        return note_name
    except Exception as e:
        logger.error("Failed to create note %s: %s", note_name, e)
        st.error(f"Failed to create note: {e}")
        return None


def auto_save_note() -> None:
    """Auto-save note content on text area change."""
    if st.session_state.current_note_filename:
        # Get the current content from the text area
        editor_key = f"note_editor_{st.session_state.current_note_filename}" if st.session_state.current_note_filename else "note_editor_empty"
        current_content = st.session_state.get(editor_key, "")
        
        # Save to file
        if save_note_content(st.session_state.current_note_filename, current_content):
            st.session_state.current_note_content = current_content
            logger.debug("Auto-saved note: %s", st.session_state.current_note_filename)


# Page title
st.markdown(
    """
    <h3 style='text-align: left; font-size: 22px; font-weight: bold; margin-top: 20px;'>Reading and Think</h3>
    """,
    unsafe_allow_html=True,
)

# Create two columns: Calibre viewer (left) and Note manager (right)
calibre_col, notes_col = st.columns([1, 1])

# ===== Left Column: Calibre Viewer =====
with calibre_col:
    # Embed Calibre in iframe
    calibre_url = st.session_state.get("CALIBRE_SERVER_URL", "")
    if calibre_url:
        container_height = st.session_state.get("CONTAINER_HEIGHT", 1000)
        iframe_html = f"""
        <iframe 
            src="{calibre_url}" 
            style="width: 100%; height: {container_height}px; border: 1px solid #ddd; border-radius: 8px;"
            allowfullscreen>
        </iframe>
        """
        st.markdown(iframe_html, unsafe_allow_html=True)

# ===== Right Column: Note Manager =====
with notes_col:
    # Get list of note files
    note_files = list_note_files()
    
    # Create two columns: Editor (left) and Notes Management (right)
    col_editor, col_management = st.columns([2, 1])
    
    # ===== Note Editor Column =====
    with col_editor:
        # Note editor
        if st.session_state.current_note_filename:
            st.markdown(f"#### :material/description: Editing: `{st.session_state.current_note_filename}`")
            
            # Auto-save indicator
            st.caption(":material/check_circle: Auto-save enabled")
            
            # Text area for note content (subtract 100px from CONTAINER_HEIGHT for UI elements)
            container_height = st.session_state.get("CONTAINER_HEIGHT", 1000) - 100
            editor_key = f"note_editor_{st.session_state.current_note_filename}" if st.session_state.current_note_filename else "note_editor_empty"
            note_content = st.text_area(
                "Note Content",
                value=st.session_state.current_note_content,
                height=container_height,
                key=editor_key,
                label_visibility="collapsed",
                help="Write your notes here in Markdown format",
                on_change=auto_save_note,
            )
        else:
            st.info("Select or create a note to start editing.")
    
    # ===== Notes Management Column =====
    with col_management:
        st.markdown("#### :material/folder: Notes Management")
        
        # My Notes section (no container)
        st.markdown('<span style="font-size: 14px; font-weight: bold;">📁 My Notes</span>', unsafe_allow_html=True)
        
        if note_files:
            # Create selectbox for note selection
            selected_note = st.selectbox(
                "Select a note to edit:",
                options=note_files,
                key="note_selectbox",
                label_visibility="collapsed",
            )
            
            # Action buttons
            col1, col2 = st.columns(2)
            with col1:
                # Download button
                st.download_button(
                    label=":material/download:",
                    data=st.session_state.current_note_content,
                    file_name=st.session_state.current_note_filename,
                    mime="text/markdown",
                    key="download_note_btn",
                    help="Download the note file",
                    use_container_width=True,
                )
            with col2:
                # Delete button
                delete_btn = st.popover(":material/delete:", use_container_width=True)
                with delete_btn:
                    st.write(f"Delete `{st.session_state.current_note_filename}`?")
                    st.write("This action cannot be undone.")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Cancel", key="cancel_popover_btn", use_container_width=True):
                            st.rerun()
                    with col2:
                        if st.button(
                            "Delete",
                            key="confirm_delete_btn_popover",
                            type="primary",
                            use_container_width=True,
                        ):
                            if delete_note_file(st.session_state.current_note_filename):
                                st.success(f"Note deleted!")
                                st.session_state.current_note_filename = None
                                st.session_state.current_note_content = ""
                                st.rerun()
            
            # Load selected note if different from current
            if selected_note != st.session_state.current_note_filename:
                st.session_state.current_note_filename = selected_note
                st.session_state.current_note_content = load_note_content(selected_note)
                st.rerun()
        else:
            st.info("No notes found.")
            st.session_state.current_note_filename = None
            st.session_state.current_note_content = ""
        
        # Create New Note section
        st.markdown("---")
        st.markdown('<span style="font-size: 14px; font-weight: bold;">:material/add_circle: Create New Note</span>', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text_input(
                "Note Name",
                value=st.session_state.new_note_name,
                placeholder="e.g., Network Fundamentals",
                max_chars=40,
                key="new_note_name_input",
                help="Enter a name for your new note (.md will be added automatically)",
                on_change=lambda: st.session_state.update(
                    {"new_note_name": st.session_state.new_note_name_input}
                ),
                label_visibility="collapsed",
            )
        with col2:
            st.button(
                ":material/add:",
                key="create_note_btn",
                on_click=create_new_note,
                help="Create a new note file",
                use_container_width=True,
            )
