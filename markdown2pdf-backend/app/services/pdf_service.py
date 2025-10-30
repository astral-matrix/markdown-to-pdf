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

# Path to custom CSS files for PDF output
_STYLES_CSS_PATH = (
    Path(__file__).resolve().parent.parent / "static" / "css" / "styles.css"
)

_CODE_HIGHLIGHT_CSS_PATH = (
    Path(__file__).resolve().parent.parent / "static" / "css" / "code-highlight.css"
)

def _read_styles_css() -> str:
    """Return the contents of ``styles.css`` and  ``code-highlight.css`` if files exists."""
    try:
        return _STYLES_CSS_PATH.read_text(encoding="utf-8")

    except OSError:
        return ""

def _read_code_highlight_css() -> str:
    """Return the contents of ``styles.css`` and  ``code-highlight.css`` if files exists."""
    try:
        return _CODE_HIGHLIGHT_CSS_PATH.read_text(encoding="utf-8")

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

code, pre {{
  font-family: '{monospace_font}', 'DejaVu Sans Mono', monospace;
}}

"""

# ---------------------------------------------------------------------------
# Mapping helpers
# ---------------------------------------------------------------------------
_FONT_STACKS = {
    # Apple SF-style fonts
    "Inter": "Inter, -apple-system, BlinkMacSystemFont, 'DejaVu Sans', sans-serif",
    "AlbertSans": "AlbertSans, 'Albert Sans', -apple-system, BlinkMacSystemFont, 'DejaVu Sans', sans-serif",
    "HankenGrotesk": "HankenGrotesk, 'Hanken Grotesk', -apple-system, BlinkMacSystemFont, 'DejaVu Sans', sans-serif",
    # Futura-style fonts (geometric sans serif)
    "Jost": "Jost, Futura, 'Futura PT', 'Century Gothic', 'DejaVu Sans', sans-serif",
    "Spartan": "Spartan, Futura, 'Futura PT', 'Century Gothic', 'DejaVu Sans', sans-serif",
    "Formera": "Formera, 'Futura Renner', Futura, 'Futura PT', 'Century Gothic', 'DejaVu Sans', sans-serif",
    # Helvetica Neue-style fonts
    "Archivo": "Archivo, 'Helvetica Neue', Helvetica, 'DejaVu Sans', sans-serif",
    "Manrope": "Manrope, 'Helvetica Neue', Helvetica, 'DejaVu Sans', sans-serif",
    "Barlow": "Barlow, 'Helvetica Neue', Helvetica, 'DejaVu Sans', sans-serif",
    # Other high-quality fonts
    "OpenSans": "OpenSans, 'Open Sans', 'DejaVu Sans', sans-serif",
    "Lato": "Lato, 'DejaVu Sans', sans-serif",
    "NunitoSans": "NunitoSans, 'Nunito Sans', 'DejaVu Sans', sans-serif",
    "IBMPlexSans": "IBMPlexSans, 'IBM Plex Sans', 'DejaVu Sans', sans-serif",
    "Roboto": "Roboto, 'DejaVu Sans', sans-serif",
    "SourceCodePro": "SourceCodePro, 'DejaVu Sans Mono', monospace",
    "MesloLGS": "MesloLGS, 'DejaVu Sans Mono', monospace",
    # System fonts
    "Helvetica": "Helvetica, Arial, sans-serif",
    "Times-Roman": "'Times New Roman', Times, serif",
    "Courier": "Courier, monospace",
    "Serif": "serif",
}

_SIZE_LEVELS = {1: 9, 2: 12, 3: 14, 4: 16, 5: 20}

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
        
        # Build CSS with font settings for PDF generation (use system paths)
        css = self._build_css(request, for_preview=False)
        html_doc = markdown_service.convert_to_html(
            request.markdown, 
            css=css, 
            include_index=getattr(request, 'include_index', False),
            add_page_breaks=getattr(request, 'add_page_breaks', False)
        )

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
        
        # Build CSS with font settings for preview (use web paths)
        css = self._build_css(request, for_preview=True)
        html_doc = markdown_service.convert_to_html(
            request.markdown, 
            css=css, 
            include_index=getattr(request, 'include_index', False),
            add_page_breaks=getattr(request, 'add_page_breaks', False)
        )

        return html_doc

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_css(self, request: PDFGenerationRequest, for_preview: bool = False) -> str:
        base_size = _SIZE_LEVELS.get(getattr(request, "size_level", 3), 12)

        # `spacing` may be an Enum or a raw string; normalise to lowercase string
        spacing_attr = getattr(request, "spacing", "normal")
        spacing_key = spacing_attr.name.lower() if hasattr(spacing_attr, "name") else str(spacing_attr).lower()
        line_height = _SPACING_LEVELS.get(spacing_key, 1.4)

        requested_font = getattr(request, "font_family", "Inter")
        font_stack = _FONT_STACKS.get(requested_font, "'DejaVu Sans', sans-serif")
        font_face_css = font_service.get_font_face_css(requested_font, for_preview=for_preview)
        
        # Get the monospace font to use for code blocks
        monospace_font = font_service.get_monospace_font()

        body_css = _BODY_CSS_TEMPLATE.format(
            font_stack=font_stack,
            base_size=base_size,
            line_height=line_height,
            monospace_font=monospace_font
        )

        css_parts = [_PAGE_CSS]
        theme_css = _read_styles_css() + _read_code_highlight_css()
        if font_face_css:
            css_parts.append(font_face_css)
        if theme_css:
            css_parts.append(theme_css)
        css_parts.append(body_css)
        
        # Add preview-specific CSS for page breaks
        if for_preview:
            preview_css = self._get_preview_specific_css()
            css_parts.append(preview_css)
            
        return "\n".join(css_parts)

    def _get_preview_specific_css(self) -> str:
        """Return CSS styles specific to preview mode to make page breaks visible."""
        return """
/* Preview-specific styles for page breaks */
.page-break {
    /* For preview: add visual representation of page break */
    margin-top: 12em !important;
    margin-bottom: 2.85em !important;
    padding-bottom: 1.25em !important;
    border-bottom: 2px dashed #ccc !important;
    position: relative !important;
}

.page-break::after {
    content: "— Page Break —" !important;
    display: block !important;
    text-align: center !important;
    color: #999 !important;
    margin-top: 1em !important;
    font-size: 0.7rem !important;
    font-style: italic !important;
}

/* Override the print-specific page-break-after for preview */
.page-break {
    page-break-after: auto !important;
}

/* PDF PREVIEW MODE ONLY */
/* Indicate page breaks before h1 heading when index is included */
/* page-break-heading is added to h1 headings when index is included */

h1.page-break-heading {
  position: relative;  /* needed for absolute positioning */
  margin-top: 8em !important;
  margin-bottom: 0.5em !important;
  padding-top: 1.5em !important;
  padding-bottom: 0em !important;
  border-top: 2px dashed #ccc !important;
}

h1.page-break-heading::before {
  content: "— Page Break —";
  position: absolute;
  top: -3em !important;         /* controls how far above the border it sits */
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.7rem;     /* smaller than the h1 font-size */
  font-weight: normal;     /* optional: not bold like h1 */
  font-style: italic !important;
  color: #888;
}

"""


# Singleton instance
pdf_service = PDFService()
