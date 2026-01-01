"""
GNS3 Notes Tools

This module provides LangChain tools for managing GNS3 project notes.
These tools can be used both as LangChain tools and as direct function calls.
"""

import json
from typing import Any

from dotenv import load_dotenv
from langchain.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun

from gns3_copilot.gns3_client.custom_gns3fy import Gns3Connector, Project
from gns3_copilot.gns3_client.gns3_notes_manager import (
    GNS3NotesManager,
)
from gns3_copilot.log_config import setup_tool_logger

# Configure logging
logger = setup_tool_logger("gns3_notes_tools")

# Load environment variables
dotenv_loaded = load_dotenv()
if dotenv_loaded:
    logger.info(
        "GNS3 Notes Tools Successfully loaded environment variables from .env file"
    )
else:
    logger.warning(
        "GNS3 Notes Tools No .env file found or failed to load. Using existing environment variables."
    )


class ListNotesTool(BaseTool):
    """
    Tool to list all notes in a GNS3 project.

    This tool retrieves and lists all notes stored in the specified GNS3 project,
    optionally including deleted notes.
    """

    name: str = "list_gns3_notes"
    description: str = """
    Lists all notes in a GNS3 project.

    Input parameters:
    - project_id: The unique UUID identifier of project (required)
    - include_deleted: If True, include deleted notes (default: False)

    Returns: List of notes with metadata including:
    - notes: Array of note objects with filename, title, created_at, updated_at
    - count: Total number of notes returned

    Example output:
        {
            "success": true,
            "notes": [
                {
                    "filename": "network_config.md",
                    "title": "Network Configuration",
                    "created_at": "2024-01-01T12:00:00Z",
                    "updated_at": "2024-01-01T12:00:00Z"
                }
            ],
            "count": 1
        }
    """

    def _run(
        self,
        tool_input: Any = None,
        run_manager: CallbackManagerForToolRun | None = None,
    ) -> dict:
        """
        Execute the list notes operation.

        Args:
            tool_input: Dictionary containing project_id and optional include_deleted
            run_manager: Run manager for tool execution (optional)

        Returns:
            Dictionary with list of notes and metadata
        """
        logger.info("Received input: %s", tool_input)

        try:
            # Validate input
            if not tool_input or "project_id" not in tool_input:
                return {
                    "success": False,
                    "error": "Missing required parameter: project_id",
                }

            project_id = tool_input["project_id"]
            include_deleted = tool_input.get("include_deleted", False)

            # Create project instance
            project = _create_project_from_id(project_id)
            if isinstance(project, dict):
                return project

            # Ensure project is open
            if project.status != "opened":
                project.open()

            # Create notes manager and list notes
            notes_manager = GNS3NotesManager(project)
            notes = notes_manager.list_notes(include_deleted=include_deleted)

            # Convert NoteInfo objects to dictionaries
            notes_list = [
                {
                    "filename": note.filename,
                    "title": note.title,
                    "created_at": note.created_at,
                    "updated_at": note.updated_at,
                }
                for note in notes
            ]

            result = {
                "success": True,
                "notes": notes_list,
                "count": len(notes_list),
            }

            logger.info("List notes result: %s", result)

            return result

        except Exception as e:
            logger.error("Error listing notes: %s", str(e))
            return {
                "success": False,
                "error": f"Failed to list notes: {str(e)}",
            }


class ReadNoteTool(BaseTool):
    """
    Tool to read a note's content from a GNS3 project.
    """

    name: str = "read_gns3_note"
    description: str = """
    Reads the content of a specific note in a GNS3 project.

    Input parameters:
    - project_id: The unique UUID identifier of project (required)
    - filename: The filename of the note to read (required, must end with .md)

    Returns: Note content and metadata including:
    - content: The markdown content of the note
    - filename: The note's filename
    - title: The note's title
    - created_at: When the note was created
    - updated_at: When the note was last updated

    Example output:
        {
            "success": true,
            "content": "# Network Configuration\n...",
            "filename": "network_config.md",
            "title": "Network Configuration",
            "created_at": "2024-01-01T12:00:00Z",
            "updated_at": "2024-01-01T12:00:00Z"
        }
    """

    def _run(
        self,
        tool_input: Any = None,
        run_manager: CallbackManagerForToolRun | None = None,
    ) -> dict:
        """
        Execute the read note operation.

        Args:
            tool_input: Dictionary containing project_id and filename
            run_manager: Run manager for tool execution (optional)

        Returns:
            Dictionary with note content and metadata
        """
        logger.info("Received input: %s", tool_input)

        try:
            # Validate input
            if not tool_input:
                return {
                    "success": False,
                    "error": "Missing required parameters: project_id and filename",
                }

            project_id = tool_input.get("project_id")
            filename = tool_input.get("filename")

            if not project_id:
                return {
                    "success": False,
                    "error": "Missing required parameter: project_id",
                }

            if not filename:
                return {
                    "success": False,
                    "error": "Missing required parameter: filename",
                }

            # Create project instance
            project = _create_project_from_id(project_id)
            if isinstance(project, dict):
                return project

            # Ensure project is open
            if project.status != "opened":
                project.open()

            # Create notes manager and read note
            notes_manager = GNS3NotesManager(project)

            try:
                content = notes_manager.read_note(filename)
            except FileNotFoundError:
                return {
                    "success": False,
                    "error": f"Note '{filename}' not found",
                }
            except ValueError as e:
                return {
                    "success": False,
                    "error": str(e),
                }

            # Get note info from index
            notes = notes_manager.list_notes()
            note_info = None
            for note in notes:
                if note.filename == filename:
                    note_info = note
                    break

            result = {
                "success": True,
                "content": content,
                "filename": filename,
                "title": note_info.title if note_info else filename[:-3],
                "created_at": note_info.created_at if note_info else "N/A",
                "updated_at": note_info.updated_at if note_info else "N/A",
            }

            logger.info("Read note result: %s", result)

            return result

        except Exception as e:
            logger.error("Error reading note: %s", str(e))
            return {
                "success": False,
                "error": f"Failed to read note: {str(e)}",
            }


class WriteNoteTool(BaseTool):
    """
    Tool to write or update a note in a GNS3 project.
    """

    name: str = "write_gns3_note"
    description: str = """
    Creates or updates a note in a GNS3 project.

    Input parameters:
    - project_id: The unique UUID identifier of project (required)
    - filename: The filename for the note (required, must end with .md)
    - content: The markdown content of the note (required)
    - title: Optional title for the note (defaults to filename without extension)

    Returns: Operation result and note metadata including:
    - success: Whether the operation succeeded
    - filename: The note's filename
    - title: The note's title
    - created_at: When the note was created (or N/A if updating)
    - updated_at: When the note was last updated
    - message: Status message

    Example output (create):
        {
            "success": true,
            "operation": "created",
            "filename": "network_config.md",
            "title": "Network Configuration",
            "created_at": "2024-01-01T12:00:00Z",
            "updated_at": "2024-01-01T12:00:00Z",
            "message": "Note 'network_config.md' created successfully"
        }

    Example output (update):
        {
            "success": true,
            "operation": "updated",
            "filename": "network_config.md",
            "title": "Network Configuration (Updated)",
            "created_at": "2024-01-01T12:00:00Z",
            "updated_at": "2024-01-01T13:00:00Z",
            "message": "Note 'network_config.md' updated successfully"
        }
    """

    def _run(
        self,
        tool_input: Any = None,
        run_manager: CallbackManagerForToolRun | None = None,
    ) -> dict:
        """
        Execute the write note operation.

        Args:
            tool_input: Dictionary containing project_id, filename, content, and optional title
            run_manager: Run manager for tool execution (optional)

        Returns:
            Dictionary with operation result and metadata
        """
        logger.info("Received input: %s", tool_input)

        try:
            # Validate input
            if not tool_input:
                return {
                    "success": False,
                    "error": "Missing required parameters: project_id, filename, and content",
                }

            project_id = tool_input.get("project_id")
            filename = tool_input.get("filename")
            content = tool_input.get("content")
            title = tool_input.get("title")

            if not project_id:
                return {
                    "success": False,
                    "error": "Missing required parameter: project_id",
                }

            if not filename:
                return {
                    "success": False,
                    "error": "Missing required parameter: filename",
                }

            if not content:
                return {
                    "success": False,
                    "error": "Missing required parameter: content",
                }

            # Validate filename
            if not filename.endswith(".md"):
                return {
                    "success": False,
                    "error": "Filename must end with .md",
                }

            # Create project instance
            project = _create_project_from_id(project_id)
            if isinstance(project, dict):
                return project

            # Ensure project is open
            if project.status != "opened":
                project.open()

            # Create notes manager
            notes_manager = GNS3NotesManager(project)

            # Check if note exists to determine operation type
            notes = notes_manager.list_notes()
            existing_note = None
            for note in notes:
                if note.filename == filename:
                    existing_note = note
                    break

            # Write note
            notes_manager.write_note(filename=filename, content=content, title=title)

            # Get updated note info
            updated_notes = notes_manager.list_notes()
            note_info = None
            for note in updated_notes:
                if note.filename == filename:
                    note_info = note
                    break

            operation = "updated" if existing_note else "created"

            result = {
                "success": True,
                "operation": operation,
                "filename": filename,
                "title": note_info.title if note_info else title,
                "created_at": note_info.created_at if note_info else "N/A",
                "updated_at": note_info.updated_at if note_info else "N/A",
                "message": f"Note '{filename}' {operation} successfully",
            }

            logger.info("Write note result: %s", result)

            return result

        except ValueError as e:
            logger.error("Validation error writing note: %s", str(e))
            return {
                "success": False,
                "error": str(e),
            }
        except Exception as e:
            logger.error("Error writing note: %s", str(e))
            return {
                "success": False,
                "error": f"Failed to write note: {str(e)}",
            }


class DeleteNoteTool(BaseTool):
    """
    Tool to delete a note from a GNS3 project.
    """

    name: str = "delete_gns3_note"
    description: str = """
    Deletes a note from a GNS3 project.

    Input parameters:
    - project_id: The unique UUID identifier of project (required)
    - filename: The filename of the note to delete (required)
    - soft_delete: If True, mark as deleted (default: True).
                    If False, permanently remove the note.

    Returns: Operation result including:
    - success: Whether the operation succeeded
    - operation: "soft_deleted" or "hard_deleted"
    - filename: The deleted note's filename
    - message: Status message

    Example output (soft delete):
        {
            "success": true,
            "operation": "soft_deleted",
            "filename": "network_config.md",
            "message": "Note 'network_config.md' soft deleted successfully"
        }

    Example output (hard delete):
        {
            "success": true,
            "operation": "hard_deleted",
            "filename": "network_config.md",
            "message": "Note 'network_config.md' permanently deleted"
        }
    """

    def _run(
        self,
        tool_input: Any = None,
        run_manager: CallbackManagerForToolRun | None = None,
    ) -> dict:
        """
        Execute the delete note operation.

        Args:
            tool_input: Dictionary containing project_id, filename, and optional soft_delete
            run_manager: Run manager for tool execution (optional)

        Returns:
            Dictionary with operation result
        """
        logger.info("Received input: %s", tool_input)

        try:
            # Validate input
            if not tool_input:
                return {
                    "success": False,
                    "error": "Missing required parameters: project_id and filename",
                }

            project_id = tool_input.get("project_id")
            filename = tool_input.get("filename")
            soft_delete = tool_input.get("soft_delete", True)

            if not project_id:
                return {
                    "success": False,
                    "error": "Missing required parameter: project_id",
                }

            if not filename:
                return {
                    "success": False,
                    "error": "Missing required parameter: filename",
                }

            # Create project instance
            project = _create_project_from_id(project_id)
            if isinstance(project, dict):
                return project

            # Ensure project is open
            if project.status != "opened":
                project.open()

            # Create notes manager and delete note
            notes_manager = GNS3NotesManager(project)

            try:
                notes_manager.delete_note(filename=filename, soft_delete=soft_delete)
            except FileNotFoundError:
                return {
                    "success": False,
                    "error": f"Note '{filename}' not found",
                }

            operation = "soft_deleted" if soft_delete else "hard_deleted"

            result = {
                "success": True,
                "operation": operation,
                "filename": filename,
                "message": f"Note '{filename}' {'soft deleted' if soft_delete else 'permanently deleted'}",
            }

            logger.info("Delete note result: %s", result)

            return result

        except Exception as e:
            logger.error("Error deleting note: %s", str(e))
            return {
                "success": False,
                "error": f"Failed to delete note: {str(e)}",
            }


def _create_project_from_id(project_id: str) -> Project | dict:
    """
    Helper function to create a Project instance from project_id.

    Args:
        project_id: The project ID to create a Project instance for

    Returns:
        Project instance or error dictionary
    """
    import os

    try:
        # Get environment variables
        api_version_str = os.getenv("API_VERSION")
        server_url = os.getenv("GNS3_SERVER_URL")

        if not api_version_str:
            return {
                "success": False,
                "error": "API_VERSION environment variable not set",
            }

        if not server_url:
            return {
                "success": False,
                "error": "GNS3_SERVER_URL environment variable not set",
            }

        # Create connector based on API version
        if api_version_str == "2":
            connector = Gns3Connector(
                url=server_url,
                api_version=int(api_version_str),
            )
        elif api_version_str == "3":
            connector = Gns3Connector(
                url=server_url,
                user=os.getenv("GNS3_SERVER_USERNAME"),
                cred=os.getenv("GNS3_SERVER_PASSWORD"),
                api_version=int(api_version_str),
            )
        else:
            return {
                "success": False,
                "error": f"Unsupported API_VERSION: {api_version_str}. Must be 2 or 3",
            }

        # Create project instance
        project = Project(project_id=project_id, connector=connector)
        project.get(get_nodes=False, get_links=False, get_stats=False)

        if not project.name:
            return {
                "success": False,
                "error": f"Project with ID '{project_id}' not found",
            }

        return project

    except Exception as e:
        logger.error("Error creating project instance: %s", str(e))
        return {
            "success": False,
            "error": f"Failed to create project instance: {str(e)}",
        }


if __name__ == "__main__":
    # Example usage
    import sys
    from pathlib import Path

    # Add src to path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

    # Example: List notes
    list_tool = ListNotesTool()
    result = list_tool._run(
        tool_input={"project_id": "2245149a-71c8-4387-9d1f-441a683ef7e7"}
    )
    print("List Notes Result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # Example: Write note
    write_tool = WriteNoteTool()
    result = write_tool._run(
        tool_input={
            "project_id": "2245149a-71c8-4387-9d1f-441a683ef7e7",
            "filename": "test_note.md",
            "content": "# Test Note\n\nThis is a test note.",
            "title": "Test Note",
        }
    )
    print("\nWrite Note Result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # Example: Read note
    read_tool = ReadNoteTool()
    result = read_tool._run(
        tool_input={
            "project_id": "2245149a-71c8-4387-9d1f-441a683ef7e7",
            "filename": "test_note.md",
        }
    )
    print("\nRead Note Result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # Example: Delete note
    delete_tool = DeleteNoteTool()
    result = delete_tool._run(
        tool_input={
            "project_id": "2245149a-71c8-4387-9d1f-441a683ef7e7",
            "filename": "test_note.md",
            "soft_delete": False,
        }
    )
    print("\nDelete Note Result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
