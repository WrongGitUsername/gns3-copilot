"""
Markdown Editor Module for GNS3 Copilot Notes Feature.

This module provides an integrated Markdown editor for taking notes and documenting
GNS3 network configurations, topologies, and troubleshooting procedures directly
within the GNS3 Copilot interface using GNS3 API.

Features:
- Full-featured Markdown editor with syntax highlighting
- Auto-save with debouncing
- Split-view editor and preview
- Project-specific note storage in GNS3 project directory via API
- Single note download and delete functionality

Usage:
    from gns3_copilot.ui_model.notes import render_notes_editor
    render_notes_editor(project, project_name)
"""

import time
from typing import Any

import streamlit as st
from streamlit_ace import st_ace  # type: ignore[import-untyped]

from gns3_copilot.gns3_client import Project
from gns3_copilot.log_config import setup_logger

logger = setup_logger("notes")

# Constants
DEFAULT_NOTE = "notes.md"
AUTO_SAVE_DELAY = 2.0  # seconds


def _load_note_content(project: Project, filename: str) -> str:
    """
    Load content of a note using Project.get_file().

    Args:
        project: GNS3 Project instance with connector and project_id set
        filename: Name of the note file

    Returns:
        Note content as string
    """
    try:
        return project.get_file(filename)
    except FileNotFoundError:
        # File doesn't exist yet, return empty string
        return ""
    except Exception as e:
        logger.error(f"Failed to load note {filename}: {e}")
        return ""


def _save_note_content(
    project: Project,
    filename: str,
    content: str,
) -> bool:
    """
    Save content to a note using Project.write_file().

    Args:
        project: GNS3 Project instance with connector and project_id set
        filename: Name of the note file
        content: Content to save

    Returns:
        True if save was successful, False otherwise
    """
    try:
        project.write_file(filename, content)
        return True
    except Exception as e:
        logger.error(f"Failed to save note {filename}: {e}")
        return False


def _delete_note_file(project: Project, filename: str) -> bool:
    """
    Delete a note by writing empty content.

    Args:
        project: GNS3 Project instance with connector and project_id set
        filename: Name of the note to delete

    Returns:
        True if deletion was successful, False otherwise
    """
    if not filename:
        return False

    try:
        # Write empty content to "delete" the note
        project.write_file(filename, "")
        return True
    except Exception as e:
        logger.error(f"Failed to delete note {filename}: {e}")
        st.error(f"Failed to delete note: {e}")
        return False


def render_notes_editor(project: Project, project_name: str | None = None) -> None:
    """
    Render the integrated Markdown notes editor using GNS3 API.

    This function provides a complete notes editing interface with:
    - Markdown editor with syntax highlighting
    - Live preview panel
    - Auto-save functionality
    - Single note download functionality
    - Note deletion functionality

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

    # Validate project
    if not project.connector or not project.project_id:
        st.error(
            "Project not properly initialized. "
            "Please select a GNS3 project to enable notes."
        )
        return

    # Show project info
    project_display_name = project_name or project.name or "Unknown Project"
    st.info(
        f"Notes are stored in GNS3 project '{project_display_name}' via API. "
        "Your notes are synced with the GNS3 server."
    )

    # Main editor layout
    st.markdown(f"### Editing: `{DEFAULT_NOTE}`")

    # Action buttons row
    col_download, col_save, col_delete = st.columns([1, 1, 1], gap="small")

    with col_download:
        if st.button(
            "Download",
            key="btn_download_note",
            use_container_width=True,
            help="Download this note as a .md file",
        ):
            # Prepare download button
            content = st.session_state.notes_content
            st.download_button(
                label=f"Download {DEFAULT_NOTE}",
                data=content,
                file_name=DEFAULT_NOTE,
                mime="text/markdown",
                key=f"download_{DEFAULT_NOTE}",
            )

    with col_save:
        if st.button(
            "Save",
            key="btn_manual_save",
            use_container_width=True,
            help="Save manually",
        ):
            if _save_note_content(
                project, DEFAULT_NOTE, st.session_state.notes_content
            ):
                st.success("Saved successfully!")
                st.session_state.notes_last_save = time.time()
            else:
                st.error("Failed to save note.")

    with col_delete:
        if st.button(
            "Delete",
            key="btn_delete_note",
            use_container_width=True,
            help="Delete current note",
        ):
            if _delete_note_file(project, DEFAULT_NOTE):
                st.success(f"Deleted '{DEFAULT_NOTE}'")
                st.session_state.notes_content = ""
                st.rerun()

    # Split view: Editor (left) and Preview (right)
    col_editor, col_preview = st.columns([1, 1], gap="medium")

    with col_editor:
        st.subheader("Editor")

        # Auto-save status indicator
        elapsed = time.time() - st.session_state.notes_last_save
        if elapsed < AUTO_SAVE_DELAY:
            st.caption(f"Auto-saving in {AUTO_SAVE_DELAY - elapsed:.1f}s...")
        else:
            st.caption("All changes saved")

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
            saved_content = _load_note_content(project, DEFAULT_NOTE)
            if content != saved_content:
                if _save_note_content(project, DEFAULT_NOTE, content):
                    st.session_state.notes_last_save = current_time
                    logger.info(f"Auto-saved: {DEFAULT_NOTE}")

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
            "notes_files": [DEFAULT_NOTE],
            "storage_location": "gns3_api",
            "project_id": None,
        }

    # With simplified file manager, we just track the default note
    return {
        "notes_count": 1,
        "notes_files": [DEFAULT_NOTE],
        "storage_location": "gns3_api",
        "project_id": project.project_id,
    }
