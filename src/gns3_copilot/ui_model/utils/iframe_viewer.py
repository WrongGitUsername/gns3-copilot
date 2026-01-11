"""
Iframe viewer component for embedding external content.

This module provides a reusable iframe viewer component that can be
embedded in any Streamlit page to display external web content.
"""

import streamlit as st


def render_iframe_viewer(
    url: str | None = None,
    height: int = 1000,
    title: str = "",
) -> None:
    """
    Render an iframe viewer component.

    Args:
        url: The URL to display in the iframe. If None, will try to get
             from session state with key "CALIBRE_SERVER_URL".
        height: The height of the iframe in pixels. Defaults to 1000.
        title: Optional title to display above the iframe.
    """
    # Get URL from parameter or session state
    if url is None:
        url = st.session_state.get("CALIBRE_SERVER_URL", "")

    # Get container height from session state if available
    if "CONTAINER_HEIGHT" in st.session_state:
        height = st.session_state["CONTAINER_HEIGHT"]

    # Display title if provided
    if title:
        st.markdown(f"#### {title}")

    # Render iframe if URL is available
    if url:
        iframe_html = f"""<iframe
            src="{url}"
            style="width: 100%; height: {height}px; border: 1px solid #ddd; border-radius: 8px;"
            allowfullscreen>
        </iframe>
        """
        st.markdown(iframe_html, unsafe_allow_html=True)
    else:
        st.warning(":material/warning: No URL configured for the iframe viewer.")
