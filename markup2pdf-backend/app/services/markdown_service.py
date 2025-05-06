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
   can inject page / font sizing rules that depend on the user’s selections.
"""
from __future__ import annotations

import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.tables import TableExtension


# ---------- helpers ---------------------------------------------------------

_GLYPH_MAP: dict[str, str] = {
    "\u2013": "-",   # en dash
    "\u2014": "-",   # em dash
    "\u00a0": " ",  # nbsp → normal space
    "\u2018": "'",   # left single quote
    "\u2019": "'",   # right single quote
    "\u201c": '"',   # left double quote
    "\u201d": '"',   # right double quote
}

def sanitize_glyphs(text: str) -> str:
    for bad, good in _GLYPH_MAP.items():
        text = text.replace(bad, good)
    return text


class MarkdownService:
    """Singleton service that converts Markdown to HTML."""

    _extensions = [
        TableExtension(),
        CodeHiliteExtension(css_class="code-highlight", pygments_style="github-dark"),
    ]

    def convert_to_html(self, markdown_text: str, css: str | None = None) -> str:
        """Return **full HTML** (optionally wrapped with a `<style>` tag)."""
        cleaned = sanitize_glyphs(markdown_text)
        html_body = markdown.markdown(cleaned, extensions=self._extensions)
        if css:
            return f"""
<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <style>
    {css}
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