"""
Notes Manager for GNS3 Copilot.

This module provides utilities for managing notes in GNS3 projects,
including reading, writing, listing, deleting, and renaming notes.

Features:
- List all note files in a GNS3 project
- Read note content
- Write note content
- Delete notes
- Rename notes
- Generate default note filenames
"""

import re
from datetime import datetime
from typing import Any

from gns3_copilot.gns3_client import (
    Gns3Connector,
    Project,
    get_gns3_connector,
)
from gns3_copilot.gns3_client.gns3_file_index import add_file_to_index, get_file_list
from gns3_copilot.log_config import setup_logger

logger = setup_logger("notes_manager")


class NotesManager:
    """Manager class for handling notes in GNS3 projects."""

    def __init__(self, project_id: str):
        """
        Initialize the NotesManager.

        Args:
            project_id: The GNS3 project UUID
        """
        self.project_id = project_id
        self.connector: Gns3Connector | None = None
        self.project: Project | None = None

    def _connect(self) -> bool:
        """
        Establish connection to GNS3 server and create project instance.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            if self.connector is None:
                connector = get_gns3_connector()
                if connector is None:
                    logger.error("Failed to create GNS3 connector")
                    return False
                self.connector = connector

            if self.project is None:
                self.project = Project(
                    project_id=self.project_id, connector=self.connector
                )

            return True
        except Exception as e:
            logger.error("Failed to connect to GNS3 server: %s", e)
            return False

    def _validate_project_id(self, project_id: str) -> bool:
        """
        Validate project_id format (UUID).

        Args:
            project_id: The project ID to validate

        Returns:
            True if valid UUID format, False otherwise
        """
        uuid_pattern = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
        return bool(re.match(uuid_pattern, project_id))

    def list_notes(self) -> list[dict[str, Any]]:
        """
        List all note files in the project.

        Returns:
            List of dictionaries containing note information:
            [{"filename": "note1.md", "content_preview": "...", "size": 123}, ...]
        """
        if not self._validate_project_id(self.project_id):
            logger.error("Invalid project_id format: %s", self.project_id)
            return []

        if not self._connect():
            logger.error("Failed to connect to GNS3 server")
            return []

        try:
            if self.project is None:
                logger.error("Project not initialized")
                return []

            # Use gns3_file_index to get file list
            files = get_file_list(self.project)
            logger.info("Retrieved file list from index: %s files", len(files))

            # Filter for markdown files
            note_files = [f for f in files if f["path"].endswith(".md")]
            logger.info("Found %d markdown files", len(note_files))

            notes = []
            for file_entry in note_files:
                filename = file_entry["path"]
                try:
                    # Get file content for preview
                    content = self.project.get_file(path=filename)
                    preview = content[:100] if content else ""

                    notes.append(
                        {
                            "filename": filename,
                            "content_preview": preview,
                            "size": len(content) if content else 0,
                        }
                    )
                except Exception as e:
                    logger.warning("Failed to read note %s: %s", filename, e)
                    notes.append(
                        {
                            "filename": filename,
                            "content_preview": "[Error reading file]",
                            "size": file_entry.get("size", 0),
                        }
                    )

            return notes

        except Exception as e:
            logger.error("Failed to list notes: %s", e)
            return []

    def read_note(self, filename: str) -> dict[str, Any]:
        """
        Read a note file from the project.

        Args:
            filename: The name of the note file (e.g., "note_20260102.md")

        Returns:
            Dictionary with keys:
            - success: bool - Operation status
            - content: str - Note content (if successful)
            - error: str - Error message (if failed)
        """
        if not self._validate_project_id(self.project_id):
            error_msg = f"Invalid project_id format: {self.project_id}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

        if not self._connect():
            error_msg = "Failed to connect to GNS3 server"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

        try:
            if self.project is None:
                return {"success": False, "error": "Project not initialized"}

            content = self.project.get_file(path=filename)
            logger.info("Successfully read note: %s", filename)
            return {"success": True, "content": content}
        except Exception as e:
            error_msg = f"Failed to read note {filename}: {e}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

    def write_note(self, filename: str, content: str) -> dict[str, Any]:
        """
        Write content to a note file in the project.

        Args:
            filename: The name of the note file (e.g., "note_20260102.md")
            content: The Markdown content to write

        Returns:
            Dictionary with keys:
            - success: bool - Operation status
            - error: str - Error message (if failed)
        """
        if not self._validate_project_id(self.project_id):
            error_msg = f"Invalid project_id format: {self.project_id}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

        if not self._connect():
            error_msg = "Failed to connect to GNS3 server"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

        try:
            if self.project is None:
                return {"success": False, "error": "Project not initialized"}

            # Write file content
            self.project.write_file(path=filename, data=content)

            # Update file index
            file_size = len(str(content))
            add_file_to_index(self.project, filename, size=file_size)

            logger.info("Successfully wrote note: %s (%d bytes)", filename, file_size)
            return {"success": True}
        except Exception as e:
            error_msg = f"Failed to write note {filename}: {e}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

    def delete_note(self, filename: str) -> dict[str, Any]:
        """
        Delete a note file from the project.

        Args:
            filename: The name of the note file to delete

        Returns:
            Dictionary with keys:
            - success: bool - Operation status
            - error: str - Error message (if failed)
        """
        if not self._validate_project_id(self.project_id):
            error_msg = f"Invalid project_id format: {self.project_id}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

        if not self._connect():
            error_msg = "Failed to connect to GNS3 server"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

        try:
            # GNS3 API doesn't have a direct delete_file method
            # We need to use the project's delete_file endpoint
            # This may vary based on the gns3fy implementation
            logger.warning("Delete operation may not be fully supported by GNS3 API")
            return {
                "success": False,
                "error": "Delete operation not supported by GNS3 API",
            }
        except Exception as e:
            error_msg = f"Failed to delete note {filename}: {e}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

    def rename_note(self, old_filename: str, new_filename: str) -> dict[str, Any]:
        """
        Rename a note file in the project.

        Note: GNS3 API doesn't support direct rename, so we implement
        this by reading the old file and writing to the new file.

        Args:
            old_filename: The current filename
            new_filename: The new filename

        Returns:
            Dictionary with keys:
            - success: bool - Operation status
            - error: str - Error message (if failed)
        """
        # Read the old file
        read_result = self.read_note(old_filename)
        if not read_result["success"]:
            return {
                "success": False,
                "error": read_result.get("error", "Failed to read old file"),
            }

        # Write to the new file
        write_result = self.write_note(new_filename, read_result["content"])
        if not write_result["success"]:
            return {
                "success": False,
                "error": write_result.get("error", "Failed to write new file"),
            }

        # Note: We can't delete the old file due to API limitations
        logger.warning(
            "Renamed note from %s to %s (old file not deleted due to API limitations)",
            old_filename,
            new_filename,
        )

        return {
            "success": True,
            "warning": "Old file not deleted due to API limitations",
        }

    @staticmethod
    def generate_default_filename() -> str:
        """
        Generate a default note filename based on current date.

        Returns:
            Filename in format: note_YYYYMMDD.md
        """
        date_str = datetime.now().strftime("%Y%m%d")
        return f"note_{date_str}.md"

    @staticmethod
    def is_valid_filename(filename: str) -> bool:
        """
        Validate note filename.

        Args:
            filename: The filename to validate

        Returns:
            True if valid, False otherwise
        """
        # Check if filename ends with .md
        if not filename.endswith(".md"):
            return False

        # Check for invalid characters
        invalid_chars = ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]
        for char in invalid_chars:
            if char in filename:
                return False

        return True


def get_notes_manager(project_id: str) -> NotesManager | None:
    """
    Factory function to create a NotesManager instance.

    Args:
        project_id: The GNS3 project UUID

    Returns:
        NotesManager instance if project_id is valid, None otherwise
    """
    manager = NotesManager(project_id)
    if manager._validate_project_id(project_id):
        return manager
    return None


if __name__ == "__main__":
    # Test the notes manager
    import pprint

    print("=" * 80)
    print("Testing NotesManager")
    print("=" * 80)

    # Replace with actual project UUID
    test_project_id = "1445a4ba-4635-430b-a332-bef438f65932"

    manager = get_notes_manager(test_project_id)
    if manager:
        print("\nList Notes:")
        notes = manager.list_notes()
        pprint.pprint(notes)

        if notes:
            print("\nRead First Note:")
            result = manager.read_note(notes[0]["filename"])
            pprint.pprint(result)

        print("\nGenerate Default Filename:")
        print(manager.generate_default_filename())

        print("\nValidate Filenames:")
        test_filenames = ["note_20260102.md", "invalid.md", "invalid/name.md"]
        for fname in test_filenames:
            print(f"  {fname}: {manager.is_valid_filename(fname)}")
    else:
        print("Failed to create NotesManager (invalid project_id)")
