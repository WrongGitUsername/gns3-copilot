import streamlit as st
import sqlite3
from datetime import datetime
from langgraph.checkpoint.sqlite import SqliteSaver # 假设使用 SQLite Checkpointer

# --- 数据库配置 ---
# 确保元数据和 LangGraph 状态使用不同的文件，实现彻底解耦
METADATA_DB_PATH = "session_metadata.sqlite"
LANGGRAPH_DB_PATH = "langgraph_checkpoints.sqlite" 

# --- 核心缓存函数 ---

@st.cache_resource
def get_metadata_db_conn():
    """
    缓存并返回元数据数据库连接 (SQLite)。
    此数据库专门用于存储 thread_id 和名称的映射。
    """
    conn = sqlite3.connect(METADATA_DB_PATH)
    # 确保元数据表存在
    conn.execute("""
        CREATE TABLE IF NOT EXISTS threads_metadata (
            thread_id TEXT PRIMARY KEY,
            name TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    return conn

#@st.cache_resource
#def get_langgraph_checkpointer():
#    """
#    缓存 LangGraph Checkpointer 实例。
#    此函数可被修改以使用 Redis/DynamoDB 等其他 Checkpointer。
#    """
#    # 初始化 LangGraph Checkpointer 专用的连接
#    conn = sqlite3.connect(LANGGRAPH_DB_PATH)
#    checkpointer = SqliteSaver(conn=conn)
#    return checkpointer

# --- 元数据 CRUD 操作函数 ---

def get_all_threads_metadata(conn: sqlite3.Connection) -> list[dict]:
    """
    读取所有会话 ID 和名称，按创建时间降序排序。
    """
    cursor = conn.execute("SELECT thread_id, name FROM threads_metadata ORDER BY created_at DESC")
    return [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]

def create_new_thread_metadata(conn: sqlite3.Connection, thread_id: str, initial_name: str):
    """
    在元数据表中插入新的会话记录。
    """
    timestamp = datetime.now().isoformat()
    conn.execute(
        "INSERT INTO threads_metadata (thread_id, name, created_at) VALUES (?, ?, ?)",
        (thread_id, initial_name, timestamp)
    )
    conn.commit()

def update_thread_name(conn: sqlite3.Connection, thread_id: str, new_name: str):
    """
    更新现有会话的名称。
    用于 LLM 自动命名后更新记录。
    """
    conn.execute(
        "UPDATE threads_metadata SET name = ? WHERE thread_id = ?",
        (new_name, thread_id)
    )
    conn.commit()