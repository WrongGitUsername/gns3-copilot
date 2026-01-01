"""
GNS3 Notes Manager

This module provides a notes management system that uses GNS3 API to store
and retrieve notes within a GNS3 project.
"""

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime

from .custom_gns3fy import Project


@dataclass
class NoteInfo:
    """Information about a note."""

    filename: str
    title: str
    created_at: str
    updated_at: str
    deleted: bool = False


@dataclass
class NotesIndex:
    """Index of all notes in the project."""

    notes: list[NoteInfo] = field(default_factory=list)


class GNS3NotesManager:
    """
    Manager for GNS3 project notes using GNS3 API.

    This class provides methods to create, read, update, delete and list notes
    stored in a GNS3 project. All notes are stored as markdown files in the
    project's notes directory, with an index file maintaining metadata.

    Attributes:
        project: The GNS3 Project instance
        index_path: Path to the notes index file
        notes_dir: Directory where note files are stored
    """

    def __init__(self, project: Project) -> None:
        """
        Initialize the notes manager.

        Args:
            project: GNS3 Project instance with connector and project_id set

        Raises:
            ValueError: If project connector or project_id is not set
        """
        if project.connector is None:
            raise ValueError("Project connector must be set")
        if project.project_id is None:
            raise ValueError("Project ID must be set")

        self.project = project
        self.index_path = "gns3_notes_index.json"
        # Store notes directly in project root with a prefix
        self.note_prefix = "gns3_note_"

    def _load_index(self) -> NotesIndex:
        """
        Load the notes index from the project.

        Returns:
            NotesIndex: The loaded index, or a new empty one if it doesn't exist

        Raises:
            ValueError: If index file contains invalid JSON
        """
        try:
            index_content = self.project.get_file(path=self.index_path)
            index_data = json.loads(index_content)

            notes = []
            for note_data in index_data.get("notes", []):
                notes.append(NoteInfo(**note_data))

            return NotesIndex(notes=notes)
        except Exception:
            # If file doesn't exist or is corrupted, return empty index
            return NotesIndex()

    def _save_index(self, index: NotesIndex) -> None:
        """
        Save the notes index to the project.

        Args:
            index: The NotesIndex to save

        Raises:
            ValueError: If failed to serialize index to JSON
        """
        try:
            index_data = {"notes": [asdict(note) for note in index.notes]}
            self.project.write_file(
                path=self.index_path, data=json.dumps(index_data, indent=2)
            )
        except Exception as e:
            raise ValueError(f"Failed to save notes index: {str(e)}") from e

    def list_notes(self, include_deleted: bool = False) -> list[NoteInfo]:
        """
        List all notes in the project.

        Args:
            include_deleted: If True, include deleted notes in the list

        Returns:
            List of NoteInfo objects, sorted by updated_at (newest first)
        """
        index = self._load_index()

        notes = index.notes
        if not include_deleted:
            notes = [note for note in notes if not note.deleted]

        # Sort by updated_at (newest first)
        notes.sort(key=lambda x: x.updated_at, reverse=True)

        return notes

    def read_note(self, filename: str) -> str:
        """
        Read a note's content from the project.

        Args:
            filename: The filename of the note to read

        Returns:
            The note's content as a string

        Raises:
            FileNotFoundError: If the note file doesn't exist
            ValueError: If the note is marked as deleted
        """
        # Load notes index to check if note exists and is not deleted
        index = self._load_index()
        note_info = None

        for note in index.notes:
            if note.filename == filename:
                note_info = note
                break

        if note_info is None:
            raise FileNotFoundError(f"Note '{filename}' not found in index")

        if note_info.deleted:
            raise ValueError(f"Note '{filename}' has been deleted")

        try:
            note_path = f"{self.note_prefix}{filename}"
            content = self.project.get_file(path=note_path)
            return content
        except Exception as e:
            raise FileNotFoundError(
                f"Failed to read note '{filename}': {str(e)}"
            ) from e

    def write_note(self, filename: str, content: str, title: str | None = None) -> None:
        """
        Write or update a note in the project.

        Args:
            filename: The filename for the note (must end with .md)
            content: The note's content
            title: Optional title for the note (defaults to filename without extension)

        Raises:
            ValueError: If filename is invalid or title not provided
        """
        if not filename.endswith(".md"):
            raise ValueError("Filename must end with .md")

        if title is None:
            title = filename[:-3]  # Remove .md extension

        index = self._load_index()
        timestamp = datetime.utcnow().isoformat() + "Z"

        # Check if note already exists
        existing_note = None
        for note in index.notes:
            if note.filename == filename:
                existing_note = note
                break

        if existing_note:
            # Update existing note
            if existing_note.deleted:
                existing_note.deleted = False  # Undelete if it was deleted
            existing_note.title = title
            existing_note.updated_at = timestamp
        else:
            # Create new note
            new_note = NoteInfo(
                filename=filename,
                title=title,
                created_at=timestamp,
                updated_at=timestamp,
                deleted=False,
            )
            index.notes.append(new_note)

        # Save the note content
        note_path = f"{self.note_prefix}{filename}"
        self.project.write_file(path=note_path, data=content)

        # Update the index
        self._save_index(index)

    def delete_note(self, filename: str, soft_delete: bool = True) -> None:
        """
        Delete a note from the project.

        Args:
            filename: The filename of the note to delete
            soft_delete: If True, mark as deleted (default). If False,
                        clear content and remove from index.

        Raises:
            FileNotFoundError: If the note doesn't exist
        """
        index = self._load_index()
        note_to_delete = None

        for note in index.notes:
            if note.filename == filename:
                note_to_delete = note
                break

        if note_to_delete is None:
            raise FileNotFoundError(f"Note '{filename}' not found in index")

        if soft_delete:
            # Mark as deleted
            note_to_delete.deleted = True
            note_to_delete.updated_at = datetime.utcnow().isoformat() + "Z"
        else:
            # Hard delete: clear content and remove from index
            note_path = f"{self.note_prefix}{filename}"
            try:
                self.project.write_file(path=note_path, data="")
            except Exception:
                pass  # Ignore errors when clearing content

            index.notes.remove(note_to_delete)

        # Update the index
        self._save_index(index)
