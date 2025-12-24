"""GNS3 Web UI Workspace page.

This module provides the workspace page that embeds the GNS3 Server Web UI
using an iframe, allowing users to interact with GNS3 directly within the
GNS3 Copilot interface.

The workspace page displays the GNS3 Web UI for the project currently selected
in the Chat page. The selected project is retrieved from the agent state.
"""

import os
import uuid

import streamlit as st

from gns3_copilot.agent import agent
from gns3_copilot.ui_model.styles import get_styles
from gns3_copilot.ui_model.utils.config_manager import get_config


def main() -> None:
    """Render the workspace page with GNS3 Web UI iframe."""
    # Apply styles
    st.markdown(get_styles(), unsafe_allow_html=True)

    # Set wide layout for more iframe width
    st.set_page_config(
        page_title="GNS3 Copilot",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Get GNS3 URL from configuration
    config_dict = get_config()
    gns3_server_url = config_dict.get("gns3", {}).get("url", "http://127.0.0.1:3080")

    # Initialize thread_id if not exists
    if "thread_id" not in st.session_state:
        st.session_state["thread_id"] = str(uuid.uuid4())

    current_thread_id = st.session_state["thread_id"]

    # Get current thread_id from session state (may be changed by session selection in chat)
    selected_thread_id = st.session_state.get("current_thread_id", current_thread_id)

    # Build config for agent state access
    config = {
        "configurable": {
            "thread_id": selected_thread_id,
            "max_iterations": 50,
        },
        "recursion_limit": 28,
    }

    # Get selected project from agent state
    snapshot = agent.get_state(config)
    selected_project = snapshot.values.get("selected_project")

    # Display iframe if project is selected in chat
    if selected_project:
        project_id = selected_project[1]  # (name, p_id, dev_count, link_count, status)

        # Build correct iframe URL
        iframe_url = f"{gns3_server_url}/static/web-ui/server/1/project/{project_id}"

        # Embed GNS3 Web UI using HTML for full width control
        iframe_html = f"""
        <iframe
            src="{iframe_url}"
            width=2000"
            height="1000"
            frameborder="0"
            scrolling="yes"
            style="border-radius: 8px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);"
        ></iframe>
        """
        st.markdown(iframe_html, unsafe_allow_html=True)
    else:
        # Show placeholder when no project is selected
        st.warning("⚠️ No project selected")
        st.info(
            """
            Please go to the **Chat** page and select a project to view its GNS3 Web UI here.

            1. Navigate to **Chat** from the sidebar
            2. Select an opened project (🟢) to enter the conversation context
            3. Return to this **Workspace** page to view the GNS3 Web UI
            """
        )


if __name__ == "__main__":
    main()
