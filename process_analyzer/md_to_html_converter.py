"""
Simple MD to HTML Converter

Minimal converter for transforming Markdown documents to HTML format.
"""

import os
import re
from typing import Optional

try:
    import markdown
except ImportError as e:
    raise ImportError(
        "Required package not found. Please install: pip install markdown"
    ) from e


class MDToHTMLConverter:
    """
    Simple converter for Markdown to HTML conversion.

    Features:
    - Convert Markdown files to HTML using markdown library
    - Basic CSS styling
    - Generate complete HTML documents
    """

    def __init__(self):
        """Initialize the converter with basic markdown extensions."""
        # Initialize markdown with basic extensions
        self.md = markdown.Markdown(
            extensions=[
                'fenced_code',     # Code blocks
                'tables',          # Table support
            ]
        )

    def convert_file(self, md_path: str, html_path: str,
                    title: Optional[str] = None) -> str:
        """Convert a Markdown file to HTML."""
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                md_content = f.read()

            html_content = self.convert_content(md_content, title)

            os.makedirs(os.path.dirname(html_path), exist_ok=True)

            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            return html_path

        except FileNotFoundError as exc:
            raise FileNotFoundError(
                f"Markdown file not found: {md_path}"
            ) from exc
        except OSError as exc:
            raise OSError(
                f"Failed to convert {md_path} to HTML: {str(exc)}"
            ) from exc

    def convert_content(self, md_content: str,
                       title: Optional[str] = None) -> str:
        """Convert Markdown content to HTML."""
        if title is None:
            title = "Document"

        # Convert Markdown to HTML
        html_body = self.md.convert(md_content)

        # Add code folding functionality
        html_body = self._add_code_folding(html_body)

        # Build complete HTML
        return self._build_template(html_body, title)

    def _load_css_file(self, css_filename: str) -> str:
        """Load CSS content from local css/ directory."""
        try:
            # Get the directory where this script is located
            current_dir = os.path.dirname(os.path.abspath(__file__))
            css_path = os.path.join(current_dir, 'css', css_filename)

            with open(css_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            # Fallback to inline CSS if file not found
            print(f"Warning: CSS file not found: {css_path}, using fallback styles")
            return self._get_fallback_css(css_filename)
        except OSError as exc:
            print(f"Warning: Failed to load CSS file {css_filename}: {str(exc)}, "
                  "using fallback styles")
            return self._get_fallback_css(css_filename)

    def _get_fallback_css(self, css_filename: str) -> str:
        """Get fallback CSS content when file loading fails."""
        if css_filename == 'markdown_base.css':
            return self._get_basic_css()
        if css_filename == 'markdown_folding.css':
            return self._get_folding_css()
        return ""

    def _get_css_content(self, include_folding: bool = True) -> str:
        """Get combined CSS content from files."""
        try:
            base_css = self._load_css_file('markdown_base.css')

            if include_folding:
                folding_css = self._load_css_file('markdown_folding.css')
                return base_css + '\n\n' + folding_css

            return base_css
        except OSError as exc:
            print(f"Warning: Failed to load CSS files: {str(exc)}, "
                  "using fallback styles")
            if include_folding:
                return self._get_basic_css() + '\n\n' + self._get_folding_css()
            return self._get_basic_css()

    def _add_code_folding(self, html_content: str) -> str:
        """Add code folding functionality to all code blocks, default collapsed."""
        # Match all code blocks (with or without language identifier)
        code_pattern = r'<pre><code(?: class="language-(\w*)")?>(.*?)</code></pre>'

        def replace_code_block(match):
            language = match.group(1) if match.group(1) else ""
            code = match.group(2)

            # Preserve original class attribute
            lang_class = f' class="language-{language}"' if language else ""

            return f'''<details>
    <summary class="code-header">CODE</summary>
    <div class="code-body">
        <pre><code{lang_class}>{code}</code></pre>
    </div>
</details>'''

        return re.sub(code_pattern, replace_code_block, html_content, flags=re.DOTALL)

    def _build_template(self, content: str, title: str) -> str:
        """Build complete HTML template."""
        css_content = self._get_css_content(include_folding=True)

        return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>{css_content}</style>
</head>
<body>
    <div class="container">{content}</div>
</body>
</html>'''

    def _get_basic_css(self) -> str:
        """Get fallback basic CSS styling when CSS files are not available."""
        # This is only used as fallback when CSS files cannot be loaded
        # The actual styles are in css/markdown_base.css
        return """/* Fallback basic styles - loaded from css/markdown_base.css */"""

    def _get_folding_css(self) -> str:
        """Get fallback code block folding CSS styling when CSS files are not available."""
        # This is only used as fallback when CSS files cannot be loaded
        # The actual styles are in css/markdown_folding.css
        return """/* Fallback folding styles - loaded from css/markdown_folding.css */"""
