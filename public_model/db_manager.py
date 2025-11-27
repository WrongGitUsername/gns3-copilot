import streamlit as st
from sqlalchemy import text, exc
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from uuid import uuid4
from datetime import datetime
import pandas as pd

#thread_id = str(uuid4())

def get_metadata_connection(reset: bool = False):
    """
    Returns a Streamlit SQLConnection that is automatically reused across reruns.
    The table `threads_metadata` is created if it does not exist.

    Parameters
    ----------
    reset : bool, default False
        If True, the table is dropped and recreated (dangerous – use only for dev).

    Returns
    -------
    st.connections.SQLConnection
    """
    conn_name = "metadata_connector"
    METADATA_DB_URL = "sqlite:///session_metadata.sqlite"

    # ---------- 1. Reuse existing connection (the official way) ----------
    try:
        # st.connection with the same name returns the cached instance
        conn = st.connection(name=conn_name, type="sql", url=METADATA_DB_URL)
    except Exception as e:               # fallback for very old Streamlit versions
        conn = st.experimental_connection(name=conn_name, type="sql", url=METADATA_DB_URL)

    # ---------- 2. (Re)create the table ----------
    create_sql = """
    CREATE TABLE IF NOT EXISTS threads_metadata (
        thread_id   TEXT    PRIMARY KEY,
        name        TEXT    NOT NULL DEFAULT 'New Chat',
        created_at  TEXT    NOT NULL
    )
    """

    with conn.session as s:
        if reset:
            s.execute(text("DROP TABLE IF EXISTS threads_metadata"))
            st.toast("threads_metadata table reset")
        s.execute(text(create_sql))
        s.commit()

    return conn

def get_all_threads(conn) -> pd.DataFrame:
    """
    Fetch all thread metadata from the `threads_metadata` table, sorted by creation time (newest first).

    Parameters
    ----------
    conn : streamlit.connections.SQLConnection
        The Streamlit SQL connection object returned by `get_metadata_connection()`.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: ['thread_id', 'name', 'created_at'].
        Returns an empty DataFrame on query failure (so the app never crashes).

    Notes
    -----
    - Uses `ttl=0` to bypass Streamlit's built-in query caching and always get fresh data.
    - All SQLAlchemy errors are caught and displayed as a user-friendly Streamlit error.
    """
    try:
        # ttl=0 forces a fresh query every time (important after insert/update/delete)
        df = conn.query(
            """
            SELECT thread_id, name, created_at 
            FROM threads_metadata 
            ORDER BY created_at DESC
            """,
            ttl=0
        )
        # Ensure consistent column types and handle possible NULLs
        if not df.empty:
            df["thread_id"] = df["thread_id"].astype(str)
            df["name"] = df["name"].fillna("Untitled Chat").astype(str)
            df["created_at"] = pd.to_datetime(df["created_at"])
        return df

    except SQLAlchemyError as e:
        st.error(
            "**Database Query Error:** Could not load chat history. "
            "Check your connection and table structure.\n\n"
            f"Details: {e}"
        )
        return pd.DataFrame(columns=["thread_id", "name", "created_at"])
    
def create_new_thread(conn, thread_id: str, initial_name: str = "New Chat") -> bool:
    """
    Creates a new thread record in the `threads_metadata` table.

    Parameters
    ----------
    conn : streamlit.connections.SQLConnection
        Active Streamlit SQL connection (from get_metadata_connection()).

    thread_id : str
        Unique thread identifier (usually a UUID string).

    initial_name : str, optional
        Display name for the new thread. Defaults to "New Chat".

    Returns
    -------
    bool
        True if the thread was created successfully, False otherwise.

    Notes
    -----
    - Generates an ISO-8601 timestamp automatically.
    - Uses parameterized query to prevent SQL injection.
    - Calls `conn.reset()` on success to clear any internal query cache.
    - Provides user-friendly error messages via `st.error`.
    """
    timestamp = datetime.now().isoformat()

    try:
        with conn.session as s:
            s.execute(
                text(
                    """
                    INSERT INTO threads_metadata 
                    (thread_id, name, created_at) 
                    VALUES (:thread_id, :name, :created_at)
                    """
                ),
                params={
                    "thread_id": thread_id,
                    "name": initial_name.strip() or "New Chat",
                    "created_at": timestamp,
                },
            )
            s.commit()

        # Clear Streamlit's internal query cache so new thread appears immediately
        conn.reset()
        return True

    except IntegrityError as e:
        # Most common case: thread_id already exists (PRIMARY KEY violation)
        st.error(
            f"**Failed to create thread:** A chat with ID `{thread_id[:8]}...` already exists. "
            "This should not happen with proper UUID generation."
        )
        # Optional: show full error only in development
        if st.secrets.get("ENV", "prod") == "dev":
            st.caption(f"IntegrityError: {e}")
        return False

    except SQLAlchemyError as e:
        st.error(f"**Database Error:** Could not create new thread.\n\nDetails: {e}")
        return False

def update_thread_name(conn, thread_id: str, new_name: str) -> bool:
    """
    Updates the display name of an existing thread in the `threads_metadata` table.

    Parameters
    ----------
    conn : streamlit.connections.SQLConnection
        Active Streamlit SQL connection.

    thread_id : str
        The unique identifier of the thread to rename.

    new_name : str
        The new name for the thread (will be stripped of leading/trailing whitespace).

    Returns
    -------
    bool
        True if the thread was found and successfully renamed, False otherwise.

    Notes
    -----
    - Uses `result.rowcount` to detect whether a row was actually updated.
    - Calls `conn.reset()` on success to invalidate Streamlit's internal query cache.
    - Sanitizes the name (strips whitespace) and falls back to a safe default if empty.
    """
    new_name = (new_name or "Untitled Chat").strip()
    if not new_name:
        new_name = "Untitled Chat"

    try:
        with conn.session as s:
            result = s.execute(
                text(
                    "UPDATE threads_metadata SET name = :new_name WHERE thread_id = :thread_id"
                ),
                params={"new_name": new_name, "thread_id": thread_id},
            )
            s.commit()

        # Check if any row was actually modified
        if result.rowcount == 0:
            st.warning(
                f"No chat found with ID `{thread_id[:8]}...`. "
                "It may have been deleted or the ID is incorrect."
            )
            return False

        # Success: clear cache so the updated name appears immediately
        conn.reset()
        return True

    except SQLAlchemyError as e:
        st.error(f"Database error while renaming chat.\n\nDetails: {e}")
        return False

def delete_thread(conn, thread_id: str) -> bool:
    """
    Permanently deletes a thread and its metadata from the `threads_metadata` table.

    Parameters
    ----------
    conn : streamlit.connections.SQLConnection
        Active Streamlit SQL connection object.

    thread_id : str
        Unique identifier of the thread to delete.

    Returns
    -------
    bool
        True if the thread existed and was successfully deleted, False otherwise.

    Notes
    -----
    - Uses `result.rowcount` to confirm that a row was actually removed.
    - Calls `conn.reset()` on success to clear Streamlit's internal query cache.
    - Shows user-friendly warnings/errors instead of crashing the app.
    - You should also delete associated messages (if you have a `messages` table).
      See the extended version below if you need that.
    """
    try:
        with conn.session as s:
            result = s.execute(
                text("DELETE FROM threads_metadata WHERE thread_id = :thread_id"),
                params={"thread_id": thread_id},
            )
            s.commit()

        if result.rowcount == 0:
            st.warning(
                f"No chat found with ID `{thread_id[:8]}...`. "
                "It may have already been deleted."
            )
            return False

        # Success → invalidate cache so the deleted thread disappears instantly
        conn.reset()
        return True

    except SQLAlchemyError as e:
        st.error(f"Database error while deleting chat.\n\nDetails: {e}")
        return False

#print(delete_thread(conn, "927afd19-8998-47ba-a360-ce35944aeaf"))
#print(get_all_threads(conn))
#print(create_new_thread(conn, thread_id=str(uuid4()), initial_name="Initial Thread Name"))
#print(update_thread_name(conn, thread_id="b00b16a5-485b-4627-a7f8-db4f3c84b1cc", new_name="安乐爱拉拉"))