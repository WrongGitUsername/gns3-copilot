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
        st.warning(":material/warning: No Calibre Server URL configured")

        st.markdown("---")

        st.markdown("### 📚 How to Configure Calibre Server")

        st.markdown("**Step 1: Configure Calibre Server URL**")
        st.markdown(
            """
            Go to **:material/settings: Settings** → **Calibre & Reading Settings**
            and enter your Calibre Server URL (e.g., `http://localhost:8080`)
            """
        )

        st.markdown("**Step 2: Start Calibre Content Server**")

        with st.expander("Option 1: Start with Calibre GUI", expanded=True):
            st.markdown(
                """
                1. Open Calibre application
                2. Click **Preferences** (or **Settings** on Linux)
                3. Select **Sharing over the net** / **Content Server**
                4. Click **Start Server** button
                5. The server will start on port 8080 by default
                6. Access at: `http://localhost:8080`
                """
            )

        with st.expander("Option 2: Start from Command Line"):
            st.markdown(
                """
                ```bash
                # Start with default library on port 8080
                calibre-server --port 8080

                # Specify custom library path
                calibre-server --port 8080 /path/to/your/calibre/library

                # Start with custom username/password
                calibre-server --port 8080 --username yourname --password yourpassword
                ```
                """
            )

        st.markdown("**Step 3: Refresh the Page**")
        st.markdown(
            """
            After configuring the URL and starting the server,
            refresh this page to see the Calibre content viewer.
            """
        )

        st.info(
            """
            💡 **Tip**: You can also access the Calibre Content Server directly
            in your browser at `http://localhost:8080` to verify it's working
            before configuring it here.
            """
        )
