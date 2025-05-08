"""Generate a styled PDF from user‑supplied Markdown using WeasyPrint.

This version fixes:
* Typo in `class PDFService` header.
* `_build_css` is now a **proper class method** (not nested).
* Removed duplicate CSS append.
* Converted `Path` → `str` for `base_url`.
"""
from __future__ import annotations

import io
from pathlib import Path

from weasyprint import HTML

from app.models import PDFGenerationRequest
from app.services.markdown_service import markdown_service
from app.services.font_service import font_service

# ---------------------------------------------------------------------------
# CSS templates
# ---------------------------------------------------------------------------
_PAGE_CSS = """
@page {
  size: A4;
  margin: 25mm;
}
"""

_BODY_CSS_TEMPLATE = """
body {{
  font-family: {font_stack};
  font-size: {base_size}px;
  line-height: {line_height};
  -weasy-font-embed: embed;
}}

code, pre {{
  font-family: '{monospace_font}', 'DejaVu Sans Mono', monospace;
}}

table {{
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
}}

th, td {{
  border: 1px solid #ddd;
  padding: 0.5em;
}}

th {{ background: #f2f2f2; }}
tr:nth-child(even) {{ background: #f9f9f9; }}
"""

# ---------------------------------------------------------------------------
# Mapping helpers
# ---------------------------------------------------------------------------
_FONT_STACKS = {
    "Inter": "Inter, 'DejaVu Sans', sans-serif",
    "Roboto": "Roboto, 'DejaVu Sans', sans-serif",
    "Serif": "serif",
}

_SIZE_LEVELS = {1: 9, 2: 10.5, 3: 12, 4: 14, 5: 16}

_SPACING_LEVELS = {
    "comfort": 1.6,
    "comfortable": 1.6,
    "roomy": 1.6,
    "normal": 1.4,
    "default": 1.4,
    "compact": 1.2,
    "tight": 1.2,
}


class PDFService:
    """Convert Markdown + user preferences into a PDF (bytes)."""

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------

    def generate_pdf(self, request: PDFGenerationRequest) -> bytes:
        """Generate PDF from markdown respecting the user's styling choices."""
        # Ensure fonts are registered
        font_service.register_fonts()
        
        # Build CSS with font settings
        css = self._build_css(request)
        html_doc = markdown_service.convert_to_html(request.markup, css=css)

        # Newer WeasyPrint versions return bytes directly, older ones accept a file‑like target.
        try:
            return HTML(string=html_doc, base_url=str(Path.cwd())).write_pdf()
        except TypeError:
            # Compatibility fallback for older WeasyPrint that require a file‑like object
            pdf_buffer = io.BytesIO()
            HTML(string=html_doc, base_url=str(Path.cwd())).write_pdf(pdf_buffer)
            pdf_buffer.seek(0)
            return pdf_buffer.read()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_css(self, request: PDFGenerationRequest) -> str:
        base_size = _SIZE_LEVELS.get(getattr(request, "size_level", 3), 12)

        # `spacing` may be an Enum or a raw string; normalise to lowercase string
        spacing_attr = getattr(request, "spacing", "normal")
        spacing_key = spacing_attr.name.lower() if hasattr(spacing_attr, "name") else str(spacing_attr).lower()
        line_height = _SPACING_LEVELS.get(spacing_key, 1.4)

        font_stack = _FONT_STACKS.get(getattr(request, "font_family", "Inter"), "'DejaVu Sans', sans-serif")
        
        # Get the monospace font to use for code blocks
        monospace_font = font_service.get_monospace_font()

        body_css = _BODY_CSS_TEMPLATE.format(
            font_stack=font_stack,
            base_size=base_size,
            line_height=line_height,
            monospace_font=monospace_font
        )

        return _PAGE_CSS + body_css


# Singleton instance
pdf_service = PDFService()