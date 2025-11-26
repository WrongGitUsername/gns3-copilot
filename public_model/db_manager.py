import streamlit as st
from sqlalchemy import text, exc
from uuid import uuid4
from datetime import datetime
import pandas as pd

METADATA_DB_URL = "sqlite:///session_metadata.sqlite"
thread_id = str(uuid4())

conn = st.connection(
        name="metadata_connector",
        type="sql",
        url=METADATA_DB_URL
    )

with conn.session as s:
    s.execute(text("""
        CREATE TABLE IF NOT EXISTS threads_metadata (
            thread_id TEXT PRIMARY KEY,
            name TEXT,
            created_at TEXT
            )
    """))
    s.commit()

def get_all_threads(conn):
    """
    Queries and returns all thread metadata, including error handling.
    """
    try:
        df = conn.query(
            "SELECT thread_id, name, created_at FROM threads_metadata ORDER BY created_at DESC",
            ttl=0  # Ensure the latest data is fetched
        )
        return df
    except exc.SQLAlchemyError as e:
        # Catch any general SQLAlchemy-related error
        st.error(f"**Query Error:** Could not retrieve the thread list. Please check the database connection and table structure. Details: {e}")
        return pd.DataFrame() # Return an empty DataFrame on failure
    
def create_new_thread(conn, thread_id, initial_name):
    """
    Creates a new thread record with the given ID and name, including error handling.
    """
    timestamp = datetime.now().isoformat()
    try:
        with conn.session as s:
            s.execute(
                text("INSERT INTO threads_metadata (thread_id, name, created_at) VALUES (:id, :name, :time)"),
                params={"id": thread_id, "name": initial_name, "time": timestamp}
            )
            s.commit()
        conn.reset() # Reset cache only upon successful commit
        return True # Success
    except exc.IntegrityError:
        # Catch errors like primary key violation (thread_id already exists)
        st.error(f"**Creation Failed:** Thread ID `{thread_id[:8]}...` already exists. Please use a unique ID.")
        return False
    except exc.SQLAlchemyError as e:
        st.error(f"**Database Error:** Could not create a new thread. Details: {e}")
        return False

def update_thread_name(conn, thread_id, new_name):
    """
    Updates the name of an existing thread, including error handling and existence check.
    """
    try:
        with conn.session as s:
            result = s.execute(
                text("UPDATE threads_metadata SET name = :new_name WHERE thread_id = :id"),
                params={"new_name": new_name, "id": thread_id}
            )
            s.commit()
        
        # Check if any rows were affected (i.e., if thread_id existed)
        if result.rowcount == 0:
            # Note: For SQLite, if the ID doesn't exist, it commits fine but rowcount is 0.
            st.warning(f"**Update Warning:** No thread found with ID `{thread_id[:8]}...` to update.")
            return False
            
        conn.reset()
        return True
    except exc.SQLAlchemyError as e:
        st.error(f"**Database Error:** Could not update the thread name. Details: {e}")
        return False

def delete_thread(conn, thread_id):
    """
    Deletes the thread record corresponding to the given thread_id, including error handling.
    """
    try:
        with conn.session as s:
            result = s.execute(
                text("DELETE FROM threads_metadata WHERE thread_id = :id"),
                params={"id": thread_id}
            )
            s.commit()
            
        # Check if any rows were affected (i.e., if thread_id existed)
        if result.rowcount == 0:
            st.warning(f"**Deletion Warning:** No thread found with ID `{thread_id[:8]}...` to delete.")
            return False

        conn.reset()
        return True
    except exc.SQLAlchemyError as e:
        st.error(f"**Database Error:** Could not delete the thread. Details: {e}")
        return False

#print(delete_thread(conn, "927afd19-8998-47ba-a360-ce35944aeaf"))
#print(get_all_threads(conn))
#print(create_new_thread(conn, thread_id=str(uuid4()), initial_name="Initial Thread Name"))
#print(update_thread_name(conn, thread_id="b00b16a5-485b-4627-a7f8-db4f3c84b1cc", new_name="安乐爱拉拉"))