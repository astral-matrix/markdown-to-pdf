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

# Path to custom CSS for PDF output
_STYLES_CSS_PATH = (
    Path(__file__).resolve().parent.parent / "static" / "css" / "styles.css"
)


def _read_styles_css() -> str:
    """Return the contents of ``styles.css`` if the file exists."""
    try:
        return _STYLES_CSS_PATH.read_text(encoding="utf-8")
    except OSError:
        return ""

# ---------------------------------------------------------------------------
# CSS templates
# ---------------------------------------------------------------------------
_PAGE_CSS = """
@page {
  size: A4;
  margin: 12.5mm;
}
"""

_BODY_CSS_TEMPLATE = """
body {{
  font-family: {font_stack};
  font-size: {base_size}px;
  line-height: {line_height};
  -weasy-font-embed: embed;
}}

/* ------------------------------------------------------------------
   Body copy & inline
   ------------------------------------------------------------------ */
p {{ margin: 0 0 .8em; }}
strong, b {{ font-weight: 600; }}
em, i     {{ font-style: italic; }}
a         {{ color: var(--accent); text-decoration: none; }}
a:hover   {{ text-decoration: underline; }}

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

ul, ol {{
  margin: 1em 0;
  padding-left: 1.5em;
}}

li {{ margin: 0.25em 0; }}

h1, h2, h3, h4, h5, h6 {{
  font-weight: 600;
  line-height: 1.25;
  margin: 0; /* reset default margin */
}}


h1 {{ font-size: 2.25em;  margin-bottom: 0.7em; page-break-before: always;}}
h2 {{ font-size: 1.5em; margin-top: 1.3em; margin-bottom: 0.6em; }}
h3 {{ font-size: 1.25em; margin-top: 1.1em; margin-bottom: 0.5em; }}
h4 {{ font-size: 1.125em; margin-top: 1em; margin-bottom: .4em; }}
h5 {{ font-size: 1em; margin-top: .9em; margin-bottom: .3em; }}
h6 {{ font-size: 0.875em; margin-top: .9em; margin-bottom: .3em; }}

"""

# ---------------------------------------------------------------------------
# Mapping helpers
# ---------------------------------------------------------------------------
_FONT_STACKS = {
    "Inter": "Inter, 'DejaVu Sans', sans-serif",
    "Roboto": "Roboto, 'DejaVu Sans', sans-serif",
    "SourceCodePro": "SourceCodePro, 'DejaVu Sans Mono', monospace",
    "MesloLGS": "MesloLGS, 'DejaVu Sans Mono', monospace",
    "Helvetica": "Helvetica, Arial, sans-serif",
    "Times-Roman": "'Times New Roman', Times, serif",
    "Courier": "Courier, monospace",
    "Serif": "serif",
}

_SIZE_LEVELS = {1: 9, 2: 12, 3: 14, 4: 16, 5: 18}

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
        html_doc = markdown_service.convert_to_html(request.markdown, css=css)

        # Newer WeasyPrint versions return bytes directly, older ones accept a file‑like target.
        try:
            return HTML(string=html_doc, base_url=str(Path.cwd())).write_pdf()
        except TypeError:
            # Compatibility fallback for older WeasyPrint that require a file‑like object
            pdf_buffer = io.BytesIO()
            HTML(string=html_doc, base_url=str(Path.cwd())).write_pdf(pdf_buffer)
            pdf_buffer.seek(0)
            return pdf_buffer.read()

    def generate_pdf_preview(self, request: PDFGenerationRequest) -> str:
        """Generate HTML preview for markdown respecting the user's styling choices."""
        # Ensure fonts are registered
        font_service.register_fonts()
        
        # Build CSS with font settings
        css = self._build_css(request)
        html_doc = markdown_service.convert_to_html(request.markdown, css=css)

        return html_doc

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_css(self, request: PDFGenerationRequest) -> str:
        base_size = _SIZE_LEVELS.get(getattr(request, "size_level", 3), 12)

        # `spacing` may be an Enum or a raw string; normalise to lowercase string
        spacing_attr = getattr(request, "spacing", "normal")
        spacing_key = spacing_attr.name.lower() if hasattr(spacing_attr, "name") else str(spacing_attr).lower()
        line_height = _SPACING_LEVELS.get(spacing_key, 1.4)

        requested_font = getattr(request, "font_family", "Inter")
        font_stack = _FONT_STACKS.get(requested_font, "'DejaVu Sans', sans-serif")
        font_face_css = font_service.get_font_face_css(requested_font)
        
        # Get the monospace font to use for code blocks
        monospace_font = font_service.get_monospace_font()

        body_css = _BODY_CSS_TEMPLATE.format(
            font_stack=font_stack,
            base_size=base_size,
            line_height=line_height,
            monospace_font=monospace_font
        )

        css_parts = [_PAGE_CSS]
        extra_css = _read_styles_css()
        if extra_css:
            css_parts.append(extra_css)
        if font_face_css:
            css_parts.append(font_face_css)
        css_parts.append(body_css)          
        return "\n".join(css_parts)


# Singleton instance
pdf_service = PDFService()
