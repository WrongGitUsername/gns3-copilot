"""
Markdown Editor Component using EasyMDE.

This module provides a WYSIWYG (What You See Is What You Get) Markdown editor
for Streamlit using EasyMDE (Easy Markdown Editor) library.

Features:
- Real-time Markdown preview
- Bidirectional data binding between JavaScript and Python
- Toolbar with common formatting options
- Supports edit and preview modes
- Auto-save capability
"""

from typing import Any

import streamlit as st

# EasyMDE CSS and JavaScript libraries
EASYMDE_CSS = """
<link rel="stylesheet" href="https://unpkg.com/easymde/dist/easymde.min.css">
<style>
    .editor-toolbar {
        border-top: 1px solid #ddd !important;
        border-left: 1px solid #ddd !important;
        border-right: 1px solid #ddd !important;
    }
    .EasyMDEContainer {
        border: 1px solid #ddd !important;
    }
    .editor-preview {
        background-color: #fff !important;
    }
    .cm-s-easymde {
        background-color: #fafafa !important;
    }
</style>
"""

EASYMDE_JS = """
<script src="https://unpkg.com/easymde/dist/easymde.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
"""

# HTML template for the editor
HTML_TEMPLATE = """
<div style="margin-bottom: 10px;">
    <label for="md-editor" style="display: block; font-weight: bold; margin-bottom: 5px;"></label>
    <textarea id="md-editor"></textarea>
</div>
"""

# JavaScript for EasyMDE integration
JS_TEMPLATE = """
// Function to dynamically load external scripts
async function loadScript(src) {
    return new Promise((resolve, reject) => {
        // Check if script is already loaded
        if (document.querySelector(`script[src="${src}"]`)) {
            resolve();
            return;
        }
        const script = document.createElement('script');
        script.src = src;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
    });
}

export default async function(component) {
    const { setStateValue, parentElement, data } = component;

    // Load external libraries
    await loadScript('https://unpkg.com/easymde/dist/easymde.min.js');
    await loadScript('https://cdn.jsdelivr.net/npm/marked/marked.min.js');

    const label = parentElement.querySelector('label');
    label.innerText = data.label;

    // Initialize EasyMDE
    const textarea = parentElement.querySelector('textarea');

    // Only create EasyMDE instance if it doesn't exist
    if (!window.easyMDEInstances) {
        window.easyMDEInstances = {};
    }

    const instanceKey = data.key || 'default';
    let easyMDE = window.easyMDEInstances[instanceKey];

    if (!easyMDE) {
        // Configure EasyMDE options
        const options = {
            element: textarea,
            spellChecker: false,
            status: false,
            autofocus: false,
            autosave: {
                enabled: false,
                uniqueId: 'gns3-copilot-notes',
                delay: 1000,
            },
            toolbar: [
                'bold', 'italic', 'heading', '|',
                'quote', 'unordered-list', 'ordered-list', '|',
                'link', 'image', 'code', 'table', '|',
                'preview', 'side-by-side', 'fullscreen', '|',
                'guide'
            ],
            insertTexts: {
                horizontalRule: ['', '\\n\\n-----\\n\\n'],
                image: ['!(', ')'],
                link: ['[', '](#url#)'],
                table: ['', '\\n| Column 1 | Column 2 | Column 3 |\\n| -------- | -------- | -------- |\\n| Text     | Text     | Text     |\\n'],
            },
            placeholder: 'Start typing your notes here...',
            previewClass: 'editor-preview',
            previewRender: function(plainText, preview) {
                // Use marked.js for preview rendering
                return marked.parse(plainText);
            }
        };

        easyMDE = new EasyMDE(options);
        window.easyMDEInstances[instanceKey] = easyMDE;
    }

    // Update content only if different to avoid cursor jumping
    const currentValue = easyMDE.value();
    if (data.value !== undefined && currentValue !== data.value) {
        easyMDE.value(data.value);
    }

    // Sync on change (with debounce to avoid excessive updates)
    let timeout;
    easyMDE.codemirror.on('change', function() {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            setStateValue('value', easyMDE.value());
        }, 300);
    });

    // Sync on blur (immediate save when losing focus)
    easyMDE.codemirror.on('blur', function() {
        setStateValue('value', easyMDE.value());
    });
}
"""

# Register the component
# Note: head parameter is not supported in current Streamlit version
md_component = st.components.v2.component(
    "markdown_editor_easymde",
    html=HTML_TEMPLATE,
    js=JS_TEMPLATE,
    css=EASYMDE_CSS,
)


def markdown_editor(
    label: str,
    default: str = "",
    key: str | None = None,
    height: int | None = None,
) -> str:
    """
    Create a WYSIWYG Markdown editor using EasyMDE.

    Args:
        label: Label text for the editor
        default: Default content for the editor
        key: Unique key for the component (required for state management)
        height: Height of the editor in pixels (optional)

    Returns:
        The current Markdown content from the editor
    """
    if key is None:
        raise ValueError("Key parameter is required for markdown_editor")

    # Get current state from session state for persistence
    component_state = st.session_state.get(key, {})
    value = component_state.get("value", default)

    # Apply custom height if specified
    if height:
        st.markdown(
            f"""
            <style>
                .EasyMDEContainer .CodeMirror {{
                    height: {height}px;
                }}
                .EasyMDEContainer .editor-preview {{
                    height: {height}px;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )

    # Mount the component
    result = md_component(
        data={"label": label, "value": value, "key": key},
        key=key,
    )

    # Extract value from component result or use default
    result_value: Any = (
        getattr(result, "value", result) if result is not None else value
    )
    return str(result_value)


if __name__ == "__main__":
    # Test the markdown editor
    st.title("Markdown Editor Test")

    editor_key = "test_md_editor"
    md_content = markdown_editor(
        label="Test Markdown Editor:",
        default="# Hello World!\n\nThis is a **test** of the Markdown editor.",
        key=editor_key,
        height=400,
    )

    st.divider()
    st.subheader("Raw Markdown Output:")
    st.text(md_content)

    st.subheader("Rendered Preview:")
    st.markdown(md_content)
