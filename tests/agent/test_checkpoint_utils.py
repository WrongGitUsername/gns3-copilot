"""
Tests for checkpoint_utils module.
Contains test cases for LangGraph checkpoint utility functions.

Test Coverage:
1. TestListThreadIds
   - Basic thread ID listing functionality
   - Empty database handling
   - Thread ID ordering (most recent first)
   - Database error handling
   - Unique thread IDs only

2. TestEdgeCases
   - Non-existent checkpointer
   - Corrupted database
   - Missing checkpoints table

3. TestFixtures
   - Mock checkpointer setup
   - Test database cleanup

Total Test Cases: 10+
"""

import sqlite3
import tempfile
import pytest
from unittest.mock import Mock, MagicMock

from gns3_copilot.agent.checkpoint_utils import list_thread_ids


class TestListThreadIds:
    """Test list_thread_ids function."""
    
    def test_basic_thread_listing(self):
        """Test basic thread ID listing with multiple threads."""
        # Create mock checkpointer with database connection
        mock_checkpointer = Mock()
        
        # Create in-memory SQLite database for testing
        conn = sqlite3.connect(":memory:")
        conn.execute(
            "CREATE TABLE checkpoints (thread_id TEXT, rowid INTEGER PRIMARY KEY AUTOINCREMENT)"
        )
        
        # Insert test data
        test_threads = ["thread-1", "thread-2", "thread-3"]
        for i, thread_id in enumerate(test_threads, 1):
            conn.execute("INSERT INTO checkpoints (thread_id) VALUES (?)", (thread_id,))
            # Add multiple checkpoints per thread
            conn.execute("INSERT INTO checkpoints (thread_id) VALUES (?)", (thread_id,))
        
        conn.commit()
        mock_checkpointer.conn = conn
        
        # Test the function
        result = list_thread_ids(mock_checkpointer)
        
        # Should return unique thread IDs
        assert len(result) == 3
        assert set(result) == set(test_threads)
        
        # Should be ordered by most recent (descending rowid)
        # Last inserted should be first
        assert result[0] == "thread-3"
        
        conn.close()
    
    def test_empty_database(self):
        """Test with empty checkpoint database."""
        mock_checkpointer = Mock()
        
        conn = sqlite3.connect(":memory:")
        conn.execute(
            "CREATE TABLE checkpoints (thread_id TEXT, rowid INTEGER PRIMARY KEY AUTOINCREMENT)"
        )
        conn.commit()
        mock_checkpointer.conn = conn
        
        result = list_thread_ids(mock_checkpointer)
        
        assert result == []
        
        conn.close()
    
    def test_single_thread(self):
        """Test with single thread."""
        mock_checkpointer = Mock()
        
        conn = sqlite3.connect(":memory:")
        conn.execute(
            "CREATE TABLE checkpoints (thread_id TEXT, rowid INTEGER PRIMARY KEY AUTOINCREMENT)"
        )
        conn.execute("INSERT INTO checkpoints (thread_id) VALUES (?)", ("single-thread",))
        conn.commit()
        mock_checkpointer.conn = conn
        
        result = list_thread_ids(mock_checkpointer)
        
        assert len(result) == 1
        assert result[0] == "single-thread"
        
        conn.close()
    
    def test_duplicate_threads(self):
        """Test that duplicate thread IDs are filtered out."""
        mock_checkpointer = Mock()
        
        conn = sqlite3.connect(":memory:")
        conn.execute(
            "CREATE TABLE checkpoints (thread_id TEXT, rowid INTEGER PRIMARY KEY AUTOINCREMENT)"
        )
        
        # Insert same thread multiple times
        thread_id = "duplicate-thread"
        for _ in range(5):
            conn.execute("INSERT INTO checkpoints (thread_id) VALUES (?)", (thread_id,))
        
        conn.commit()
        mock_checkpointer.conn = conn
        
        result = list_thread_ids(mock_checkpointer)
        
        # Should return only unique thread IDs
        assert len(result) == 1
        assert result[0] == thread_id
        
        conn.close()
    
    def test_uuid_thread_ids(self):
        """Test with UUID-format thread IDs."""
        mock_checkpointer = Mock()
        
        conn = sqlite3.connect(":memory:")
        conn.execute(
            "CREATE TABLE checkpoints (thread_id TEXT, rowid INTEGER PRIMARY KEY AUTOINCREMENT)"
        )
        
        # Insert UUID-like thread IDs
        uuid_threads = [
            "550e8400-e29b-41d4-a716-446655440000",
            "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
            "6ba7b811-9dad-11d1-80b4-00c04fd430c8",
        ]
        
        for thread_id in uuid_threads:
            conn.execute("INSERT INTO checkpoints (thread_id) VALUES (?)", (thread_id,))
        
        conn.commit()
        mock_checkpointer.conn = conn
        
        result = list_thread_ids(mock_checkpointer)
        
        assert len(result) == 3
        assert set(result) == set(uuid_threads)
        
        conn.close()


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_missing_table(self):
        """Test handling of missing checkpoints table."""
        mock_checkpointer = Mock()
        
        conn = sqlite3.connect(":memory:")
        # Don't create the checkpoints table
        mock_checkpointer.conn = conn
        
        result = list_thread_ids(mock_checkpointer)
        
        # Should return empty list on error
        assert result == []
        
        conn.close()
    
    def test_database_error(self):
        """Test handling of database connection errors."""
        mock_checkpointer = Mock()
        
        # Mock a connection that raises error
        mock_conn = Mock()
        mock_conn.execute.side_effect = Exception("Database connection lost")
        mock_checkpointer.conn = mock_conn
        
        result = list_thread_ids(mock_checkpointer)
        
        # Should return empty list on error
        assert result == []
    
    def test_none_checkpointer(self):
        """Test with None checkpointer."""
        result = list_thread_ids(None)
        
        # Should return empty list on error
        assert result == []
    
    def test_missing_conn_attribute(self):
        """Test with checkpointer missing conn attribute."""
        mock_checkpointer = Mock(spec=[])  # Empty spec, no conn attribute
        
        result = list_thread_ids(mock_checkpointer)
        
        # Should return empty list on error
        assert result == []
    
    def test_corrupted_database(self):
        """Test with corrupted database."""
        mock_checkpointer = Mock()
        
        conn = sqlite3.connect(":memory:")
        conn.execute(
            "CREATE TABLE checkpoints (thread_id TEXT, rowid INTEGER PRIMARY KEY AUTOINCREMENT)"
        )
        conn.commit()
        
        # Corrupt the database by closing it
        conn.close()
        mock_checkpointer.conn = conn
        
        result = list_thread_ids(mock_checkpointer)
        
        # Should return empty list on error
        assert result == []


class TestOrdering:
    """Test thread ID ordering behavior."""
    
    def test_most_recent_first(self):
        """Test that most recent threads appear first."""
        mock_checkpointer = Mock()
        
        conn = sqlite3.connect(":memory:")
        conn.execute(
            "CREATE TABLE checkpoints (thread_id TEXT, rowid INTEGER PRIMARY KEY AUTOINCREMENT)"
        )
        
        # Insert threads in order
        threads_order = ["first-thread", "second-thread", "third-thread"]
        for thread_id in threads_order:
            conn.execute("INSERT INTO checkpoints (thread_id) VALUES (?)", (thread_id,))
        
        conn.commit()
        mock_checkpointer.conn = conn
        
        result = list_thread_ids(mock_checkpointer)
        
        # Verify order: most recent (last inserted) should be first
        assert result[0] == "third-thread"
        assert result[1] == "second-thread"
        assert result[2] == "first-thread"
        
        conn.close()
    
    def test_mixed_activity_ordering(self):
        """Test ordering with mixed activity across threads."""
        mock_checkpointer = Mock()
        
        conn = sqlite3.connect(":memory:")
        conn.execute(
            "CREATE TABLE checkpoints (thread_id TEXT, rowid INTEGER PRIMARY KEY AUTOINCREMENT)"
        )
        
        # Simulate mixed activity: Thread A, then B, then A again
        activity = [
            ("thread-a", 1),
            ("thread-b", 2),
            ("thread-a", 3),
            ("thread-c", 4),
        ]
        
        for thread_id, _ in activity:
            conn.execute("INSERT INTO checkpoints (thread_id) VALUES (?)", (thread_id,))
        
        conn.commit()
        mock_checkpointer.conn = conn
        
        result = list_thread_ids(mock_checkpointer)
        
        # Verify order: unique threads ordered by most recent activity
        # Thread-c (most recent), thread-a, thread-b
        assert len(result) == 3
        assert result[0] == "thread-c"  # Most recent
        assert result[1] == "thread-a"  # Second most recent
        assert result[2] == "thread-b"  # Oldest
        
        conn.close()


@pytest.fixture(autouse=True)
def cleanup():
    """Cleanup after tests."""
    yield
    # Any cleanup if needed
    pass
