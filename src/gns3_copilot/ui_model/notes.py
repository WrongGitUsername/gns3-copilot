"""
Notes Page for GNS3 Copilot.

This module implements the notes management page where users can create,
edit, and manage Markdown notes stored in GNS3 projects.

Features:
- Display current GNS3 project
- List all notes in the project
- Create new notes with default or custom filenames
- Edit notes with WYSIWYG Markdown editor
- Save notes to GNS3 project
- Rename notes
"""

import streamlit as st

from gns3_copilot.agent import agent
from gns3_copilot.log_config import setup_logger
from gns3_copilot.ui_model.utils.markdown_editor import markdown_editor
from gns3_copilot.ui_model.utils.notes_manager import (
    NotesManager,
    get_notes_manager,
)

logger = setup_logger("notes")

# Initialize session state for notes page
if "notes_current_file" not in st.session_state:
    st.session_state.notes_current_file = None
if "notes_content" not in st.session_state:
    st.session_state.notes_content = ""
if "notes_list" not in st.session_state:
    st.session_state.notes_list = []
if "notes_dirty_flag" not in st.session_state:
    st.session_state.notes_dirty_flag = False
if "notes_show_rename" not in st.session_state:
    st.session_state.notes_show_rename = False
if "notes_new_filename" not in st.session_state:
    st.session_state.notes_new_filename = ""


def _get_selected_project() -> tuple[str | None, str | None]:
    """
    Get the currently selected project from agent state.

    Returns:
        Tuple of (project_name, project_id) or (None, None) if no project selected
    """
    selected_thread_id = st.session_state.get("selected_thread_id")

    if selected_thread_id:
        # Historical session: get from agent state
        config = {
            "configurable": {
                "thread_id": st.session_state["current_thread_id"],
                "max_iterations": 50,
            },
            "recursion_limit": 28,
        }
        snapshot = agent.get_state(config)
        selected_p = snapshot.values.get("selected_project")
    else:
        # New session: get from temp storage
        selected_p = st.session_state.get("temp_selected_project")

    return (selected_p[0], selected_p[1]) if selected_p else (None, None)


def _refresh_notes_list(project_id: str) -> None:
    """
    Refresh the list of notes from the GNS3 project.

    Args:
        project_id: The GNS3 project UUID
    """
    manager = get_notes_manager(project_id)
    if manager:
        notes = manager.list_notes()
        st.session_state.notes_list = notes
        logger.info("Refreshed notes list: %d notes", len(notes))
    else:
        st.session_state.notes_list = []
        st.error("Failed to load notes: Invalid project ID")


def _load_note_content(project_id: str, filename: str) -> None:
    """
    Load note content from the GNS3 project.

    Args:
        project_id: The GNS3 project UUID
        filename: The note filename
    """
    manager = get_notes_manager(project_id)
    if manager:
        result = manager.read_note(filename)
        if result["success"]:
            st.session_state.notes_content = result["content"]
            st.session_state.notes_current_file = filename
            st.session_state.notes_dirty_flag = False
            logger.info("Loaded note: %s", filename)
        else:
            st.error(f"Failed to load note: {result.get('error', 'Unknown error')}")


def _save_note_content(project_id: str, filename: str, content: str) -> None:
    """
    Save note content to the GNS3 project.

    Args:
        project_id: The GNS3 project UUID
        filename: The note filename
        content: The Markdown content to save
    """
    manager = get_notes_manager(project_id)
    if manager:
        result = manager.write_note(filename, content)
        if result["success"]:
            st.session_state.notes_dirty_flag = False
            st.session_state.notes_current_file = filename
            st.success(f"Saved note: {filename}")
            logger.info("Saved note: %s (%d bytes)", filename, len(content))
            # Refresh notes list
            _refresh_notes_list(project_id)
        else:
            st.error(f"Failed to save note: {result.get('error', 'Unknown error')}")


def _rename_note(project_id: str, old_filename: str, new_filename: str) -> None:
    """
    Rename a note in the GNS3 project.

    Args:
        project_id: The GNS3 project UUID
        old_filename: The current filename
        new_filename: The new filename
    """
    manager = get_notes_manager(project_id)
    if manager:
        result = manager.rename_note(old_filename, new_filename)
        if result["success"]:
            st.success(f"Renamed note from {old_filename} to {new_filename}")
            if result.get("warning"):
                st.warning(result["warning"])
            # Update current file if it was renamed
            if st.session_state.notes_current_file == old_filename:
                st.session_state.notes_current_file = new_filename
            # Refresh notes list
            _refresh_notes_list(project_id)
        else:
            st.error(f"Failed to rename note: {result.get('error', 'Unknown error')}")


def main() -> None:
    """Main notes page function."""
    st.title(":material/note: Notes Management")

    # Get selected project
    project_name, project_id = _get_selected_project()

    # Display project information
    if project_name and project_id:
        st.info(f"**Current Project:** {project_name}")
    else:
        st.warning(
            "No project selected. Please select a project from the "
            "Chat page to manage notes."
        )
        st.stop()

    # Refresh notes list on first load or manually
    if st.button(":material/refresh: Refresh", key="refresh_notes"):
        _refresh_notes_list(project_id)

    # Initial load if list is empty
    if not st.session_state.notes_list:
        _refresh_notes_list(project_id)

    # Layout: Sidebar for notes list, Main area for editor
    col1, col2 = st.columns([1, 3], gap="medium")

    with col1:
        st.subheader(":material/list: Notes List")

        # Create new note button
        if st.button(
            ":material/add: Create New Note",
            key="create_note",
            use_container_width=True,
        ):
            default_filename = NotesManager.generate_default_filename()
            st.session_state.notes_current_file = default_filename
            st.session_state.notes_content = ""
            st.session_state.notes_dirty_flag = False
            st.session_state.notes_show_rename = False
            st.session_state.notes_new_filename = ""
            st.rerun()

        # Show custom filename input for new notes
        if st.session_state.notes_current_file and not any(
            note["filename"] == st.session_state.notes_current_file
            for note in st.session_state.notes_list
        ):
            st.markdown("**New Note Filename:**")
            custom_filename = st.text_input(
                "Filename",
                value=st.session_state.notes_current_file,
                key="new_note_filename",
            )
            if custom_filename != st.session_state.notes_current_file:
                if NotesManager.is_valid_filename(custom_filename):
                    st.session_state.notes_current_file = custom_filename
                    st.rerun()
                else:
                    st.error("Invalid filename. Must end with .md")

        # List existing notes
        if st.session_state.notes_list:
            st.markdown("---")
            for note in st.session_state.notes_list:
                filename = note["filename"]
                preview = note.get("content_preview", "")

                # Display note item
                with st.container():
                    is_current = st.session_state.notes_current_file == filename

                    if is_current:
                        st.markdown(f"**{filename}** *(current)*")
                    else:
                        st.markdown(filename)

                    # Show preview
                    if preview:
                        st.caption(f"{preview}...")

                    # Select button
                    if st.button(
                        ":material/file_open: Select",
                        key=f"select_{filename}",
                        use_container_width=True,
                        type="primary" if not is_current else "secondary",
                    ):
                        if not is_current:
                            # Warn if current note has unsaved changes
                            if st.session_state.notes_dirty_flag:
                                st.warning("Current note has unsaved changes!")
                            _load_note_content(project_id, filename)
                            st.rerun()

                    st.divider()

        else:
            st.info("No notes found. Create a new note to get started.")

    with col2:
        st.subheader(":material/edit: Editor")

        # Show current filename
        if st.session_state.notes_current_file:
            st.markdown(f"**Current File:** `{st.session_state.notes_current_file}`")
        else:
            st.markdown("**No file selected**")

        # Markdown editor
        editor_key = "notes_editor"
        md_content = markdown_editor(
            label="",
            default=st.session_state.notes_content,
            key=editor_key,
            height=500,
        )

        # Check if content has changed
        if md_content != st.session_state.notes_content:
            st.session_state.notes_content = md_content
            st.session_state.notes_dirty_flag = True

        # Action buttons
        col_btn1, col_btn2, col_btn3 = st.columns(3)

        with col_btn1:
            if st.button(
                ":material/save: Save", key="save_note", use_container_width=True
            ):
                if st.session_state.notes_current_file:
                    _save_note_content(
                        project_id,
                        st.session_state.notes_current_file,
                        st.session_state.notes_content,
                    )
                else:
                    st.error("No file selected to save")

        with col_btn2:
            if st.button(
                ":material/edit_note: Rename",
                key="rename_note_btn",
                use_container_width=True,
            ):
                if st.session_state.notes_current_file:
                    st.session_state.notes_show_rename = True
                else:
                    st.error("No file selected to rename")

        with col_btn3:
            if st.button(
                ":material/delete: Delete", key="delete_note", use_container_width=True
            ):
                if st.session_state.notes_current_file:
                    # GNS3 API doesn't support delete, show info
                    st.info(
                        "Delete operation is not supported by GNS3 API. "
                        "You can rename to keep the file organized."
                    )
                else:
                    st.error("No file selected to delete")

        # Rename dialog
        if st.session_state.notes_show_rename and st.session_state.notes_current_file:
            st.markdown("---")
            st.markdown("### Rename Note")
            new_filename = st.text_input(
                "New Filename",
                value=st.session_state.notes_current_file,
                key="rename_input",
            )

            col_rename1, col_rename2 = st.columns(2)

            with col_rename1:
                if st.button(":material/check: Confirm Rename", key="confirm_rename"):
                    if (
                        new_filename
                        and new_filename != st.session_state.notes_current_file
                    ):
                        if NotesManager.is_valid_filename(new_filename):
                            _rename_note(
                                project_id,
                                st.session_state.notes_current_file,
                                new_filename,
                            )
                            st.session_state.notes_show_rename = False
                            st.rerun()
                        else:
                            st.error("Invalid filename. Must end with .md")
                    else:
                        st.warning("Please enter a new filename")

            with col_rename2:
                if st.button(":material/close: Cancel", key="cancel_rename"):
                    st.session_state.notes_show_rename = False
                    st.rerun()

        # Show dirty flag indicator
        if st.session_state.notes_dirty_flag:
            st.warning(":material/warning: You have unsaved changes!")


if __name__ == "__main__":
    main()
