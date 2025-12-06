import streamlit as st


pg = st.navigation(
    [
        "ui_model/Settings.py",
        "ui_model/Chat.py",
        "ui_model/About.py"
    ],
    position="sidebar"
)
pg.run()