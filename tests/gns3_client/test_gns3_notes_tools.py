"""
Unit tests for GNS3 Notes Tools

This module contains tests for the LangChain tools that manage GNS3 project notes.
"""

import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gns3_copilot.gns3_client.custom_gns3fy import Project
from gns3_copilot.tools_v2.gns3_notes_tools import (
    DeleteNoteTool,
    ListNotesTool,
    ReadNoteTool,
    WriteNoteTool,
    _create_project_from_id,
)


@pytest.fixture
def mock_project():
    """Create a mock Project instance."""
    project = Mock(spec=Project)
    project.project_id = "test-project-id"
    project.name = "Test Project"
    project.status = "opened"
    project.connector = Mock()
    return project


@pytest.fixture
def mock_notes_manager():
    """Create a mock GNS3NotesManager instance."""
    manager = Mock()
    manager.list_notes.return_value = []
    return manager


class TestListNotesTool:
    """Tests for ListNotesTool class."""

    def test_list_notes_success(self, mock_project, mock_notes_manager):
        """Test successful list notes operation."""
        with patch(
            "gns3_copilot.tools_v2.gns3_notes_tools._create_project_from_id",
            return_value=mock_project,
        ), patch(
            "gns3_copilot.tools_v2.gns3_notes_tools.GNS3NotesManager",
            return_value=mock_notes_manager,
        ):
            mock_notes_manager.list_notes.return_value = []

            tool = ListNotesTool()
            result = tool._run(tool_input={"project_id": "test-project-id"})

            assert result["success"] is True
            assert "notes" in result
            assert "count" in result

    def test_list_notes_with_deleted(self, mock_project, mock_notes_manager):
        """Test listing notes including deleted ones."""
        with patch(
            "gns3_copilot.tools_v2.gns3_notes_tools._create_project_from_id",
            return_value=mock_project,
        ), patch(
            "gns3_copilot.tools_v2.gns3_notes_tools.GNS3NotesManager",
            return_value=mock_notes_manager,
        ):
            from gns3_copilot.gns3_client.gns3_notes_manager import NoteInfo

            mock_notes_manager.list_notes.return_value = [
                NoteInfo(
                    filename="note1.md",
                    title="Note 1",
                    created_at="2024-01-01T00:00:00Z",
                    updated_at="2024-01-01T00:00:00Z",
                    deleted=False,
                )
            ]

            tool = ListNotesTool()
            result = tool._run(
                tool_input={"project_id": "test-project-id", "include_deleted": True}
            )

            assert result["success"] is True
            assert len(result["notes"]) == 1

    def test_list_notes_missing_project_id(self):
        """Test list notes with missing project_id."""
        tool = ListNotesTool()
        result = tool._run(tool_input={})

        assert result["success"] is False
        assert "Missing required parameter" in result["error"]

    def test_list_notes_project_error(self):
        """Test list notes with project creation error."""
        with patch(
            "gns3_copilot.tools_v2.gns3_notes_tools._create_project_from_id",
            return_value={"success": False, "error": "Project not found"},
        ):
            tool = ListNotesTool()
            result = tool._run(tool_input={"project_id": "invalid-id"})

            assert result["success"] is False
            assert "Project not found" in result["error"]


class TestReadNoteTool:
    """Tests for ReadNoteTool class."""

    def test_read_note_success(self, mock_project, mock_notes_manager):
        """Test successful read note operation."""
        mock_notes_manager.read_note.return_value = "# Test Note\n\nContent"
        mock_notes_manager.list_notes.return_value = []

        with patch(
            "gns3_copilot.tools_v2.gns3_notes_tools._create_project_from_id",
            return_value=mock_project,
        ), patch(
            "gns3_copilot.tools_v2.gns3_notes_tools.GNS3NotesManager",
            return_value=mock_notes_manager,
        ):
            tool = ReadNoteTool()
            result = tool._run(
                tool_input={"project_id": "test-project-id", "filename": "test.md"}
            )

            assert result["success"] is True
            assert result["content"] == "# Test Note\n\nContent"
            assert result["filename"] == "test.md"

    def test_read_note_missing_parameters(self):
        """Test read note with missing parameters."""
        tool = ReadNoteTool()

        # Missing both parameters
        result = tool._run(tool_input={})
        assert result["success"] is False

        # Missing filename
        result = tool._run(tool_input={"project_id": "test-id"})
        assert result["success"] is False

        # Missing project_id
        result = tool._run(tool_input={"filename": "test.md"})
        assert result["success"] is False

    def test_read_note_not_found(self, mock_project, mock_notes_manager):
        """Test read note when note doesn't exist."""
        mock_notes_manager.read_note.side_effect = FileNotFoundError("Note not found")

        with patch(
            "gns3_copilot.tools_v2.gns3_notes_tools._create_project_from_id",
            return_value=mock_project,
        ), patch(
            "gns3_copilot.tools_v2.gns3_notes_tools.GNS3NotesManager",
            return_value=mock_notes_manager,
        ):
            tool = ReadNoteTool()
            result = tool._run(
                tool_input={"project_id": "test-project-id", "filename": "missing.md"}
            )

            assert result["success"] is False
            assert "not found" in result["error"]


class TestWriteNoteTool:
    """Tests for WriteNoteTool class."""

    def test_write_note_create(self, mock_project, mock_notes_manager):
        """Test creating a new note."""
        from gns3_copilot.gns3_client.gns3_notes_manager import NoteInfo

        # Note doesn't exist initially
        mock_notes_manager.list_notes.return_value = []

        # After writing, note exists
        mock_notes_manager.list_notes.side_effect = [
            [],  # First call - note doesn't exist
            [
                NoteInfo(
                    filename="test.md",
                    title="Test",
                    created_at="2024-01-01T00:00:00Z",
                    updated_at="2024-01-01T00:00:00Z",
                    deleted=False,
                )
            ],  # Second call - note exists
        ]

        with patch(
            "gns3_copilot.tools_v2.gns3_notes_tools._create_project_from_id",
            return_value=mock_project,
        ), patch(
            "gns3_copilot.tools_v2.gns3_notes_tools.GNS3NotesManager",
            return_value=mock_notes_manager,
        ):
            tool = WriteNoteTool()
            result = tool._run(
                tool_input={
                    "project_id": "test-project-id",
                    "filename": "test.md",
                    "content": "# Test Note",
                    "title": "Test",
                }
            )

            assert result["success"] is True
            assert result["operation"] == "created"
            mock_notes_manager.write_note.assert_called_once()

    def test_write_note_update(self, mock_project, mock_notes_manager):
        """Test updating an existing note."""
        from gns3_copilot.gns3_client.gns3_notes_manager import NoteInfo

        existing_note = NoteInfo(
            filename="test.md",
            title="Test",
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
            deleted=False,
        )

        mock_notes_manager.list_notes.side_effect = [
            [existing_note],  # First call - note exists
            [existing_note],  # Second call - note exists
        ]

        with patch(
            "gns3_copilot.tools_v2.gns3_notes_tools._create_project_from_id",
            return_value=mock_project,
        ), patch(
            "gns3_copilot.tools_v2.gns3_notes_tools.GNS3NotesManager",
            return_value=mock_notes_manager,
        ):
            tool = WriteNoteTool()
            result = tool._run(
                tool_input={
                    "project_id": "test-project-id",
                    "filename": "test.md",
                    "content": "# Updated Content",
                }
            )

            assert result["success"] is True
            assert result["operation"] == "updated"
            mock_notes_manager.write_note.assert_called_once()

    def test_write_note_invalid_filename(self):
        """Test write note with invalid filename."""
        tool = WriteNoteTool()
        result = tool._run(
            tool_input={
                "project_id": "test-project-id",
                "filename": "invalid.txt",  # Must end with .md
                "content": "# Test",
            }
        )

        assert result["success"] is False
        assert "must end with .md" in result["error"]

    def test_write_note_missing_parameters(self):
        """Test write note with missing parameters."""
        tool = WriteNoteTool()

        # Missing all parameters
        result = tool._run(tool_input={})
        assert result["success"] is False

        # Missing content
        result = tool._run(
            tool_input={"project_id": "test-id", "filename": "test.md"}
        )
        assert result["success"] is False


class TestDeleteNoteTool:
    """Tests for DeleteNoteTool class."""

    def test_delete_note_soft_delete(self, mock_project, mock_notes_manager):
        """Test soft deleting a note."""
        with patch(
            "gns3_copilot.tools_v2.gns3_notes_tools._create_project_from_id",
            return_value=mock_project,
        ), patch(
            "gns3_copilot.tools_v2.gns3_notes_tools.GNS3NotesManager",
            return_value=mock_notes_manager,
        ):
            tool = DeleteNoteTool()
            result = tool._run(
                tool_input={
                    "project_id": "test-project-id",
                    "filename": "test.md",
                    "soft_delete": True,
                }
            )

            assert result["success"] is True
            assert result["operation"] == "soft_deleted"
            mock_notes_manager.delete_note.assert_called_once_with(
                filename="test.md", soft_delete=True
            )

    def test_delete_note_hard_delete(self, mock_project, mock_notes_manager):
        """Test hard deleting a note."""
        with patch(
            "gns3_copilot.tools_v2.gns3_notes_tools._create_project_from_id",
            return_value=mock_project,
        ), patch(
            "gns3_copilot.tools_v2.gns3_notes_tools.GNS3NotesManager",
            return_value=mock_notes_manager,
        ):
            tool = DeleteNoteTool()
            result = tool._run(
                tool_input={
                    "project_id": "test-project-id",
                    "filename": "test.md",
                    "soft_delete": False,
                }
            )

            assert result["success"] is True
            assert result["operation"] == "hard_deleted"
            mock_notes_manager.delete_note.assert_called_once_with(
                filename="test.md", soft_delete=False
            )

    def test_delete_note_not_found(self, mock_project, mock_notes_manager):
        """Test delete note when note doesn't exist."""
        mock_notes_manager.delete_note.side_effect = FileNotFoundError("Note not found")

        with patch(
            "gns3_copilot.tools_v2.gns3_notes_tools._create_project_from_id",
            return_value=mock_project,
        ), patch(
            "gns3_copilot.tools_v2.gns3_notes_tools.GNS3NotesManager",
            return_value=mock_notes_manager,
        ):
            tool = DeleteNoteTool()
            result = tool._run(
                tool_input={
                    "project_id": "test-project-id",
                    "filename": "missing.md",
                }
            )

            assert result["success"] is False
            assert "not found" in result["error"]


class TestCreateProjectFromId:
    """Tests for _create_project_from_id helper function."""

    @patch.dict(os.environ, {"API_VERSION": "2", "GNS3_SERVER_URL": "http://localhost"})
    @patch("gns3_copilot.tools_v2.gns3_notes_tools.Project")
    @patch("gns3_copilot.tools_v2.gns3_notes_tools.Gns3Connector")
    def test_create_project_success(self, mock_connector, mock_project_class):
        """Test successful project creation."""
        mock_project = Mock(spec=Project)
        mock_project.name = "Test Project"
        mock_project_class.return_value = mock_project

        result = _create_project_from_id("test-project-id")

        assert isinstance(result, Mock)
        assert not isinstance(result, dict)

    @patch.dict(os.environ, {}, clear=True)
    def test_create_project_missing_api_version(self):
        """Test project creation with missing API_VERSION."""
        result = _create_project_from_id("test-project-id")

        assert isinstance(result, dict)
        assert result["success"] is False
        assert "API_VERSION" in result["error"]

    @patch.dict(os.environ, {"API_VERSION": "2"}, clear=True)
    def test_create_project_missing_server_url(self):
        """Test project creation with missing GNS3_SERVER_URL."""
        result = _create_project_from_id("test-project-id")

        assert isinstance(result, dict)
        assert result["success"] is False
        assert "GNS3_SERVER_URL" in result["error"]

    @patch.dict(
        os.environ,
        {"API_VERSION": "2", "GNS3_SERVER_URL": "http://localhost"},
    )
    @patch("gns3_copilot.tools_v2.gns3_notes_tools.Project")
    @patch("gns3_copilot.tools_v2.gns3_notes_tools.Gns3Connector")
    def test_create_project_not_found(self, mock_connector, mock_project_class):
        """Test project creation when project doesn't exist."""
        mock_project = Mock(spec=Project)
        mock_project.name = None  # Project not found
        mock_project_class.return_value = mock_project

        result = _create_project_from_id("invalid-project-id")

        assert isinstance(result, dict)
        assert result["success"] is False
        assert "not found" in result["error"].lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
