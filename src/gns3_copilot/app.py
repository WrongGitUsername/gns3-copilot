
"""
GNS3 Copilot Streamlit application entry point.

Main application module that initializes and runs the Streamlit-based web interface
with navigation between settings, chat, and help pages.
"""

import streamlit as st

NAV_PAGES = [
    "ui_model/settings.py",
    "ui_model/chat.py",
    "ui_model/help.py",
]

ABOUT_TEXT = """
GNS3 Copilot is an AI-powered assistant designed to help network engineers with
GNS3-related tasks. It leverages advanced language models to provide insights,
answer questions, and assist with network simulations.

**Features:**
- Answer GNS3-related queries
- Provide configuration examples
- Assist with troubleshooting

**Usage:**
Simply type your questions or commands in the chat interface,
and GNS3 Copilot will respond accordingly.

**Note:** This is a prototype version. For more information,
visit the [GNS3 Copilot GitHub Repository](https://github.com/yueguobin/gns3-copilot).
"""


def render_sidebar_about() -> None:
    #Dedicated function for sidebar content
    with st.sidebar:
        st.header("About")
        st.markdown(ABOUT_TEXT)


def main() -> None:
    # Set page metadata early to ensure consistent layout, title, and sidebar behavior.
    st.set_page_config(
        page_title="GNS3 Copilot",
        page_icon="",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    # Prevent the app to crash if a page path has been renamed or missing.
    try:
        pg = st.navigation(NAV_PAGES, position="sidebar")
        pg.run()
    except Exception as exc:
        st.error("Failed to initialize application navigation.")
        st.exception(exc)
        st.stop()

    render_sidebar_about()


if __name__ == "__main__":
    main()
