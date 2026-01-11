"""
Reading page for GNS3 Copilot application.

This module provides a reading interface with Calibre ebook viewer and
a multi-note management system for taking and organizing reading notes.

Features:
- Calibre ebook viewer embedded in iframe
- Multi-note management system (create, select, delete notes)
- Notes saved as Markdown files
- Download notes functionality
- Automatic notes directory creation
"""

import streamlit as st

from gns3_copilot.ui_model.utils.iframe_viewer import render_iframe_viewer
from gns3_copilot.ui_model.utils.notes_manager import (  # type: ignore[attr-defined]
    render_notes_editor,
)

# Page title
st.markdown(
    """
    <h3 style='text-align: left; font-size: 22px; font-weight: bold; margin-top: 20px;'>Reading and Think</h3>
    """,
    unsafe_allow_html=True,
)

# Create two columns: Calibre viewer (left) and Note manager (right)
calibre_col, notes_col = st.columns([1, 1])

# ===== Left Column: Calibre Viewer =====
with calibre_col:
    render_iframe_viewer()

# ===== Right Column: Note Manager =====
with notes_col:
    render_notes_editor()
