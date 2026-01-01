"""
Markdown Editor Module for GNS3 Copilot Notes Feature.

This module provides an integrated Markdown editor for taking notes and documenting
GNS3 network configurations, topologies, and troubleshooting procedures directly
within the GNS3 Copilot interface using GNS3 API.

Features:
- Full-featured Markdown editor with syntax highlighting
- File management (create, rename, delete markdown files)
- Auto-save with debouncing
- Split-view editor and preview
- Project-specific note storage in GNS3 project directory via API
- Single note download functionality

Usage:
    from gns3_copilot.ui_model.notes import render_notes_editor
    render_notes_editor(project, project_name)
"""

import time
from typing import Any

import streamlit as st
from streamlit_ace import st_ace  # type: ignore[import-untyped]

from gns3_copilot.gns3_client.custom_gns3fy import Project
from gns3_copilot.gns3_client.gns3_notes_manager import (
    GNS3NotesManager,
    NoteInfo,
)
from gns3_copilot.log_config import setup_logger

logger = setup_logger("notes")

# Constants
DEFAULT_NOTE = "notes.md"
AUTO_SAVE_DELAY = 2.0  # seconds


def _create_notes_manager(project: Project) -> GNS3NotesManager:
    """
    Create a GNS3 notes manager instance.

    Args:
        project: GNS3 Project instance with connector and project_id set

    Returns:
        GNS3NotesManager instance

    Raises:
        ValueError: If project connector or project_id is not set
    """
    return GNS3NotesManager(project)


def _list_notes_info(notes_manager: GNS3NotesManager) -> list[NoteInfo]:
    """
    List all notes using the notes manager.

    Args:
        notes_manager: GNS3NotesManager instance

    Returns:
        List of NoteInfo objects
    """
    try:
        return notes_manager.list_notes()
    except Exception as e:
        logger.error(f"Failed to list notes: {e}")
        return []


def _load_note_content(notes_manager: GNS3NotesManager, filename: str) -> str:
    """
    Load content of a note using the notes manager.

    Args:
        notes_manager: GNS3NotesManager instance
        filename: Name of the note file

    Returns:
        Note content as string
    """
    try:
        return notes_manager.read_note(filename)
    except Exception as e:
        logger.error(f"Failed to load note {filename}: {e}")
        return ""


def _save_note_content(
    notes_manager: GNS3NotesManager,
    filename: str,
    content: str,
) -> bool:
    """
    Save content to a note using the notes manager.

    Args:
        notes_manager: GNS3NotesManager instance
        filename: Name of the note file
        content: Content to save

    Returns:
        True if save was successful, False otherwise
    """
    try:
        # Use filename without .md as default title
        title = filename[:-3] if filename.endswith(".md") else filename
        notes_manager.write_note(filename, content, title=title)
        return True
    except Exception as e:
        logger.error(f"Failed to save note {filename}: {e}")
        return False


def _create_note_file(notes_manager: GNS3NotesManager, filename: str) -> bool:
    """
    Create a new note using the notes manager.

    Args:
        notes_manager: GNS3NotesManager instance
        filename: Name of the new note

    Returns:
        True if creation was successful, False otherwise
    """
    if not filename:
        return False

    # Ensure .md extension
    if not filename.endswith(".md"):
        filename += ".md"

    try:
        # Check if note already exists
        existing_notes = notes_manager.list_notes()
        for note in existing_notes:
            if note.filename == filename:
                st.warning(f"File '{filename}' already exists.")
                return False

        # Create new note with default content
        title = filename[:-3] if filename.endswith(".md") else filename
        content = f"# {title}\n\n"
        notes_manager.write_note(filename, content, title=title)
        return True
    except Exception as e:
        logger.error(f"Failed to create note {filename}: {e}")
        st.error(f"Failed to create note: {e}")
        return False


def _delete_note_file(notes_manager: GNS3NotesManager, filename: str) -> bool:
    """
    Delete a note using the notes manager.

    Args:
        notes_manager: GNS3NotesManager instance
        filename: Name of the note to delete

    Returns:
        True if deletion was successful, False otherwise
    """
    if not filename:
        return False

    try:
        notes_manager.delete_note(filename, soft_delete=True)
        return True
    except Exception as e:
        logger.error(f"Failed to delete note {filename}: {e}")
        st.error(f"Failed to delete note: {e}")
        return False


def _format_timestamp(timestamp_str: str) -> str:
    """
    Format ISO timestamp to a readable string.

    Args:
        timestamp_str: ISO format timestamp string

    Returns:
        Formatted timestamp string
    """
    try:
        from datetime import datetime

        dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return timestamp_str


def render_file_sidebar(
    notes_manager: GNS3NotesManager,
    current_file: str | None,
) -> str | None:
    """
    Render the file sidebar with note list and management buttons.

    Args:
        notes_manager: GNS3NotesManager instance
        current_file: Currently selected file

    Returns:
        Selected filename or None
    """
    st.sidebar.header("📝 Notes")

    # Show storage location indicator
    st.sidebar.caption("📁 GNS3 project (via API)")

    # List available note files
    notes_list = _list_notes_info(notes_manager)

    if not notes_list:
        st.sidebar.info("No notes found. Create your first note!")
        return None

    # Extract filenames for the selector
    notes_filenames = [note.filename for note in notes_list]

    # Display file list
    st.sidebar.subheader("Files")
    selected = st.sidebar.selectbox(
        "Select a note",
        notes_filenames,
        index=0
        if current_file is None
        else notes_filenames.index(current_file)
        if current_file in notes_filenames
        else 0,
        key="notes_file_selector",
    )

    # Show note details
    if selected:
        note_info = next((n for n in notes_list if n.filename == selected), None)
        if note_info:
            st.sidebar.caption(f"Updated: {_format_timestamp(note_info.updated_at)}")

    st.sidebar.divider()

    # Create new file
    with st.sidebar.expander("Create New Note", expanded=False):
        new_filename = st.text_input(
            "Filename",
            placeholder="e.g., config-notes",
            key="new_note_filename",
        )
        if st.button(
            ":material/add_circle:",
            key="btn_create_note",
            use_container_width=True,
            type="primary",
        ):
            if new_filename.strip():
                if _create_note_file(notes_manager, new_filename.strip()):
                    st.sidebar.success(f"Created '{new_filename}'")
                    st.rerun()
            else:
                st.sidebar.warning("Please enter a filename.")

    return selected


def render_notes_editor(project: Project, project_name: str | None = None) -> None:
    """
    Render the integrated Markdown notes editor using GNS3 API.

    This function provides a complete notes editing interface with:
    - File management sidebar
    - Markdown editor with syntax highlighting
    - Live preview panel
    - Auto-save functionality
    - Single note download functionality

    Args:
        project: GNS3 Project instance with connector and project_id set
        project_name: Name of the GNS3 project (for display)

    Side Effects:
        - Creates and manages notes in GNS3 project via API
        - Updates session state for editor content and auto-save
    """
    # Initialize session state for notes editor
    if "notes_content" not in st.session_state:
        st.session_state.notes_content = ""
    if "notes_last_save" not in st.session_state:
        st.session_state.notes_last_save = 0.0
    if "notes_file" not in st.session_state:
        st.session_state.notes_file = None

    # Validate project
    if not project.connector or not project.project_id:
        st.error(
            "Project not properly initialized. "
            "Please select a GNS3 project to enable notes."
        )
        return

    # Create notes manager
    try:
        notes_manager = _create_notes_manager(project)
    except ValueError as e:
        st.error(f"Failed to initialize notes manager: {e}")
        return

    # Show project info
    project_display_name = project_name or project.name or "Unknown Project"
    st.info(
        f"📁 Notes are stored in GNS3 project '{project_display_name}' via API. "
        "Your notes are synced with the GNS3 server.",
        icon="ℹ️",
    )

    # Render file sidebar
    current_file = render_file_sidebar(notes_manager, st.session_state.notes_file)

    # Update session state if file changed
    if current_file and current_file != st.session_state.notes_file:
        st.session_state.notes_file = current_file
        st.session_state.notes_content = _load_note_content(notes_manager, current_file)
        st.session_state.notes_last_save = 0.0

    # If no file selected, show empty state
    if not current_file:
        st.info("Select a note file from the sidebar to start editing.")
        return

    # Main editor layout
    st.markdown(f"### Editing: `{current_file}`")

    # Action buttons row
    col_download, col_save = st.columns([1, 1], gap="small")

    with col_download:
        if st.button(
            "📥 Download",
            key="btn_download_note",
            use_container_width=True,
            help="Download this note as a .md file",
        ):
            # Prepare download button
            content = st.session_state.notes_content
            st.download_button(
                label=f"Download {current_file}",
                data=content,
                file_name=current_file,
                mime="text/markdown",
                key=f"download_{current_file}",
            )

    with col_save:
        if st.button(
            ":material/save:",
            key="btn_manual_save",
            use_container_width=True,
            help="Save manually",
        ):
            if _save_note_content(
                notes_manager, current_file, st.session_state.notes_content
            ):
                st.success("Saved successfully!")
                st.session_state.notes_last_save = time.time()
            else:
                st.error("Failed to save note.")

    # Delete button
    if st.button(
        ":material/delete:",
        key="btn_delete_note",
        use_container_width=True,
        help="Delete current note",
    ):
        if _delete_note_file(notes_manager, current_file):
            st.success(f"Deleted '{current_file}'")
            st.session_state.notes_file = None
            st.session_state.notes_content = ""
            st.rerun()

    # Split view: Editor (left) and Preview (right)
    col_editor, col_preview = st.columns([1, 1], gap="medium")

    with col_editor:
        st.subheader("Editor")

        # Auto-save status indicator
        elapsed = time.time() - st.session_state.notes_last_save
        if elapsed < AUTO_SAVE_DELAY:
            st.caption(f"💾 Auto-saving in {AUTO_SAVE_DELAY - elapsed:.1f}s...")
        else:
            st.caption("💾 All changes saved")

        # Markdown editor with streamlit-ace
        content = st_ace(
            value=st.session_state.notes_content,
            language="markdown",
            theme="monokai",
            key="notes_editor",
            height=st.session_state.CONTAINER_HEIGHT - 150,
            show_gutter=True,
            wrap=True,
            auto_update=True,
            font_size=14,
        )

        # Update session state
        st.session_state.notes_content = content

        # Auto-save logic with debouncing
        current_time = time.time()
        if current_time - st.session_state.notes_last_save >= AUTO_SAVE_DELAY:
            if content != _load_note_content(notes_manager, current_file):
                if _save_note_content(notes_manager, current_file, content):
                    st.session_state.notes_last_save = current_time
                    logger.info(f"Auto-saved: {current_file}")

    with col_preview:
        st.subheader("Preview")

        # Preview container
        preview_container = st.container(
            height=st.session_state.CONTAINER_HEIGHT - 100,
            border=False,
        )

        with preview_container:
            if st.session_state.notes_content:
                st.markdown(st.session_state.notes_content)
            else:
                st.info("Start typing in the editor to see preview here...")


def get_notes_summary(project: Project) -> dict[str, Any]:
    """
    Get summary of notes for a project using GNS3 API.

    Args:
        project: GNS3 Project instance

    Returns:
        Dictionary with notes summary information
    """
    if not project.connector or not project.project_id:
        return {
            "notes_count": 0,
            "notes_files": [],
            "storage_location": "gns3_api",
            "project_id": None,
        }

    try:
        notes_manager = _create_notes_manager(project)
        notes_list = _list_notes_info(notes_manager)
        notes_files = [note.filename for note in notes_list]

        return {
            "notes_count": len(notes_files),
            "notes_files": notes_files,
            "storage_location": "gns3_api",
            "project_id": project.project_id,
        }
    except Exception as e:
        logger.error(f"Failed to get notes summary: {e}")
        return {
            "notes_count": 0,
            "notes_files": [],
            "storage_location": "gns3_api",
            "project_id": project.project_id,
        }
