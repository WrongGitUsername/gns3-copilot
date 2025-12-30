"""
Chat Helper Functions for GNS3 Copilot.

This module provides auxiliary functions for managing chat sessions,
including creating new sessions, switching between sessions, and
handling session-related UI operations.

Functions:
    new_session(): Create a new chat session by generating a unique thread ID

Example:
    from gns3_copilot.ui_model.utils import new_session

    # Create a new chat session
    session_options = [("(Please select session)", None), ...]
    new_session(session_options)
"""

import uuid

import streamlit as st

from gns3_copilot.log_config import setup_logger

logger = setup_logger("chat_helpers")


def new_session(session_options: list[tuple[str, str | None]]) -> None:
    """
    Create a new chat session by generating a unique thread ID and resetting session state.

    Initializes a fresh conversation session with a new UUID, clears existing session data,
    resets project selection, and resets the UI session selector to the default option.

    Args:
        session_options: List of tuples containing session display names and thread IDs.
                         The first element should be the default placeholder option.

    Side Effects:
        - Updates st.session_state with new thread_id
        - Clears current_thread_id, state_history, and temp_selected_project
        - Resets session_select to default option (session_options[0])
        - Logs session creation
    """
    new_tid = str(uuid.uuid4())
    # Real new thread id
    st.session_state["thread_id"] = new_tid
    # Clear selected_project from temp storage
    st.session_state["temp_selected_project"] = None
    # Clear your own state
    st.session_state["current_thread_id"] = None
    st.session_state["state_history"] = None
    # Reset the dropdown menu to the first option ("(Please select session)", None)
    st.session_state["session_select"] = session_options[0]
    logger.debug("New Session created with thread_id= %s", new_tid)


def build_topology_iframe_url(project_id: str) -> str:
    """
    Build the GNS3 topology iframe URL based on API version and URL mode.

    Constructs the appropriate iframe URL for displaying GNS3 topology,
    taking into account different API versions (v2 vs v3) and URL modes
    (login page vs project page).

    Args:
        project_id: The GNS3 project ID to embed in the iframe URL

    Returns:
        The complete iframe URL for the GNS3 topology

    Example:
        url = build_topology_iframe_url("a1b2c3d4")
        # Returns something like:
        # "http://127.0.0.1:3080/static/web-ui/server/1/project/a1b2c3d4"
    """
    # Get GNS3 server URL from session_state (loaded from .env file)
    gns3_server_url = st.session_state.get("GNS3_SERVER_URL", "http://127.0.0.1:3080/")

    # Get API version and construct appropriate iframe URL
    api_version = st.session_state.get("API_VERSION", "2")
    if api_version == "3":
        if st.session_state.gns3_url_mode == "login":
            # API v3 login page
            iframe_url = f"{gns3_server_url}"
        else:
            # API v3 uses 'controller' instead of 'server'
            iframe_url = (
                f"{gns3_server_url}/static/web-ui/controller/1/project/{project_id}"
            )
    else:
        # API v2 uses 'server' (default behavior)
        iframe_url = f"{gns3_server_url}/static/web-ui/server/1/project/{project_id}"

    return iframe_url


def generate_topology_iframe_html(
    iframe_url: str,
    zoom_scale: float,
    container_height: int,
    iframe_width: int = 2000,
    iframe_height: int = 1000,
) -> str:
    """
    Generate HTML for displaying GNS3 topology in an iframe with zoom and scroll capabilities.

    This function creates an HTML string that embeds the GNS3 topology interface
    in a scrollable container with zoom functionality. The iframe uses CSS zoom
    to maintain the correct coordinate system while scaling the content.

    Args:
        iframe_url: The URL of the GNS3 topology page to embed
        zoom_scale: The zoom scale factor (e.g., 0.7 for 70%, 0.8 for 80%)
        container_height: The height of the scroll container in pixels
        iframe_width: The width of the iframe in pixels (default: 2000)
        iframe_height: The height of the iframe in pixels (default: 1000)

    Returns:
        HTML string ready for use with st.markdown(unsafe_allow_html=True)

    Example:
        iframe_html = generate_topology_iframe_html(
            iframe_url="http://localhost:3080/static/web-ui/server/1/project/123",
            zoom_scale=0.8,
            container_height=600
        )
        st.markdown(iframe_html, unsafe_allow_html=True)
    """
    iframe_html = f"""
    <style>
        .iframe-scroll-container {{
            width: 100%;
            height: {container_height}px;
            overflow: auto;
            border: none;

            /* Use Flexbox to center the iframe vertically and horizontally */
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .iframe-scroll-container iframe {{
            width: {iframe_width}px;
            height: {iframe_height}px;
            border: none;
            /* Use zoom instead of transform to keep coordinate system correct */
            zoom: {zoom_scale};
        }}
    </style>

    <div class="iframe-scroll-container">
        <iframe
            src="{iframe_url}"
            loading="lazy"
            allowfullscreen
            title="GNS3 Topology"
        ></iframe>
    </div>
    """

    return iframe_html
