# markdown_service.py
"""Markdown to HTML conversion with built‑in glyph sanitisation.
This module converts CommonMark+GitHub‑style Markdown into styled HTML that is ready to be
handed to a PDF renderer (WeasyPrint).

Key fixes
----------
1. **Removed** the inline `<style>` injection that ReportLab was treating as literal text.
2. **Added** a `sanitize_glyphs` pass to translate problematic Unicode (curly quotes,
   em/en dashes, etc.) into safe ASCII equivalents when the chosen fonts do not contain
   the glyphs.
3. The function can optionally receive a CSS string so that the caller (our PDF service)
   can inject page / font sizing rules that depend on the user's selections.
4. **Fixed** whitespace preservation in code blocks to ensure proper formatting.
5. **Styled** code blocks with light gray background, rounded corners, and proper padding.
"""
from __future__ import annotations

import re
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions import Extension
from markdown.inlinepatterns import SubstituteTagInlineProcessor

# Import font service to get the monospace font
from app.services.font_service import font_service

# ---------- helpers ---------------------------------------------------------

_GLYPH_MAP: dict[str, str] = {
    "\u2013": "-",   # en dash
    "\u2014": "-",   # em dash
    "\u00a0": " ",  # nbsp → normal space
    "\u2018": "'",   # left single quote
    "\u2019": "'",   # right single quote
    "\u201c": '"',   # left double quote
    "\u201d": '"',   # right double quote
    "\~": '~',   # tilde
    "\&": '&amp;',   # ampersand
    "\#": '#',   # hash
    "\*": '*',   # asterisk
    "\_": '_',   # underscore
    "\+": '+',   # plus
    "\-": '-',   # dash
    "\=": '=',   # equals


}

def sanitize_glyphs(text: str) -> str:
    for bad, good in _GLYPH_MAP.items():
        text = text.replace(bad, good)
    return text

def preserve_code_block_whitespace(html: str) -> str:
    """Ensure code blocks preserve their whitespace by properly handling pre/code tags."""
    # Get the monospace font to use for code blocks
    monospace_font = font_service.get_monospace_font()
    
    # Make sure pre tags have the necessary CSS for whitespace preservation and styling
    pre_style = (
        'style="white-space: pre-wrap; word-break: keep-all; '
        'background-color: #f5f7f9; border-radius: 8px; padding: 16px; '
        f'font-family: {monospace_font}, monospace; margin: 16px 0; display: inline-block; '
        'min-width: 40%; max-width: 100%; overflow-x: auto;"'
    )
    
    html = re.sub(r'<pre>', f'<pre {pre_style}>', html)
    
    # Ensure code inside pre tags maintains its formatting
    # This mainly addresses specific formatting issues with leading spaces and newlines
    def fix_code_content(match):
        code_content = match.group(1)
        # Ensure content inside code blocks isn't unintentionally altered
        return f'<pre {pre_style}><code>{code_content}</code></pre>'
    
    # Find code blocks with content and ensure they have proper whitespace preservation
    html = re.sub(r'<pre><code>(.*?)</code></pre>', fix_code_content, html, flags=re.DOTALL)
    
    return html

# Custom extension to handle line breaks
class LineBreakExtension(Extension):
    """Extension to convert newlines to <br> tags."""
    def extendMarkdown(self, md):
        # This pattern matches newlines not in code blocks
        pattern = r'(?<!\n)\n(?!\n)'  # Match single newlines
        processor = SubstituteTagInlineProcessor(pattern, 'br')
        md.inlinePatterns.register(processor, 'linebreaks', 175)  # Priority higher than nl2br

class MarkdownService:
    """Singleton service that converts Markdown to HTML."""

    _extensions = [
        TableExtension(),
        CodeHiliteExtension(css_class="code-highlight", pygments_style="github-dark", linenums=False),
        FencedCodeExtension(),  # Explicitly add fenced code extension
        LineBreakExtension(),  # Add our custom line break extension
    ]

    def convert_to_html(self, markdown_text: str, css: str | None = None) -> str:
        """Return **full HTML** (optionally wrapped with a `<style>` tag)."""
        cleaned = sanitize_glyphs(markdown_text)
        
        # Convert markdown to HTML
        html_body = markdown.markdown(cleaned, extensions=self._extensions)
        
        # Ensure code blocks preserve whitespace
        html_body = preserve_code_block_whitespace(html_body)
        
        # Handle paragraph breaks more explicitly to ensure they render in PDF
        # This replaces double newlines with properly spaced paragraphs
        html_body = re.sub(r'</p>\s*<p>', '</p>\n\n<p>', html_body)
        
        # Ensure single line breaks within paragraphs are preserved (CommonMark treats single newlines as spaces)
        # We need to do this after markdown conversion for content not in code blocks
        html_body = re.sub(r'([^>])\n([^<])', r'\1<br>\n\2', html_body)
        
        # Get the monospace font for CSS
        monospace_font = font_service.get_monospace_font()
        
        if css:
            return f"""
<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <style>
    {css}
    pre {{
        white-space: pre-wrap;
        word-break: keep-all;
        tab-size: 4;
        -moz-tab-size: 4;
        background-color: #f5f7f9;
        border-radius: 8px;
        padding: 16px;
        font-family: {monospace_font}, monospace;
        margin: 16px 0;
        display: inline-block;
        min-width: 40%;
        max-width: 100%;
        overflow-x: auto;
    }}
    code {{
        white-space: pre-wrap;
        font-family: {monospace_font}, monospace;
    }}
    </style>
  </head>
  <body>
    {html_body}
  </body>
</html>"""
        # Caller will inject CSS later
        return html_body


# Expose a ready‑to‑use instance
markdown_service = MarkdownService()