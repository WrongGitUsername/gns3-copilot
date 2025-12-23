"""
GNS3 Copilot Streamlit application entry point.

Main application module that initializes and runs the Streamlit-based web interface
with navigation between settings, chat, and help pages.
"""

import streamlit as st
from gns3_copilot.utils.updater import is_update_available, save_skipped_version, load_skipped_version

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


def perform_update_check():
    """Perform the actual update check synchronously."""
    try:
        available, current, latest = is_update_available()
        if available:
            return {
                "status": "available",
                "current": current,
                "latest": latest
            }
        else:
            return {
                "status": "up_to_date",
                "current": current,
                "latest": latest
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def check_and_display_updates():
    """Check for updates and display results - runs once on startup."""
    
    # Skip if already checked in this session
    if "startup_update_checked" in st.session_state:
        return
    
    # Mark as checked immediately to prevent re-running
    st.session_state["startup_update_checked"] = True
    
    # Perform the check with a spinner
    with st.spinner("🔄 Checking for updates..."):
        result = perform_update_check()
        st.session_state["startup_update_result"] = result
    
    # Force a rerun to display the result
    st.rerun()

def render_startup_update_result():
    """Display the startup update check result if available."""
    result = st.session_state.get("startup_update_result")
    if not result:
        return

    status = result.get("status")

    # Update available
    if status == "available":
        latest = result["latest"]

        # Session dismiss
        if st.session_state.get("_update_dismissed"):
            return

        # Persistent skip
        skipped_version = st.session_state.get("skipped_update_version")
        if skipped_version == latest:
            return

        # Render warning FIRST
        st.warning(
            f"⚠️ **Update available:** {result['current']} → {latest}\n\n"
            "Go to **Settings → GNS3 Copilot Updates** to update."
        )

        # Render actions BELOW the warning
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Dismiss", key="dismiss_update"):
                st.session_state["_update_dismissed"] = True
                st.rerun()

        with col2:
            if st.button("Skip this version", key="skip_update"):
                st.session_state["skipped_update_version"] = latest
                save_skipped_version(latest)
                st.rerun()

    # Up to date
    elif status == "up_to_date":
        if st.session_state.get("_up_to_date_dismissed"):
            return

        st.success(f"✅ You're using the latest version ({result['current']})")

        if st.button("Dismiss", key="dismiss_uptodate"):
            st.session_state["_up_to_date_dismissed"] = True
            st.rerun()

    # Error encountered
    elif status == "error":
        if st.session_state.get("_error_dismissed"):
            return

        st.error(
            f"❌ Update check failed: {result.get('error', 'Unknown error')}"
        )

        if st.button("Dismiss", key="dismiss_error"):
            st.session_state["_error_dismissed"] = True
            st.rerun()

def render_sidebar_about() -> None:
    """Render the About section in the sidebar."""
    with st.sidebar:
        st.header("About")
        st.markdown(ABOUT_TEXT)


def main() -> None:
    """Main application entry point."""
    # Set page metadata early to ensure consistent layout
    st.set_page_config(
        page_title="GNS3 Copilot",
        layout="centered",
        initial_sidebar_state="expanded",
    )
    
    if "skipped_update_version" not in st.session_state:
        st.session_state["skipped_update_version"] = load_skipped_version()
        
    # Check for updates on startup (blocking, runs once)
    check_and_display_updates()
    
    # Display update result at the top
    render_startup_update_result()
    
    # Prevent the app from crashing if a page path is missing
    try:
        pg = st.navigation(NAV_PAGES, position="sidebar")
        pg.run()
    except Exception as exc:
        st.error("Failed to initialize application navigation.")
        st.exception(exc)
        st.stop()
    
    # Render sidebar content
    render_sidebar_about()


if __name__ == "__main__":
    main()
