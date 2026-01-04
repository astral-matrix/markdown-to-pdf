"""Font registration and lookup helpers for PDF/preview rendering."""
# pylint: disable=line-too-long,too-many-branches,too-many-return-statements,broad-exception-caught,no-else-return
from typing import List
import os
from pathlib import Path
from reportlab.pdfbase import pdfmetrics  # type: ignore[import-untyped]
from reportlab.pdfbase.ttfonts import TTFont  # type: ignore[import-untyped]


class FontService:
    """Manage available fonts and resolve font faces for styles."""
    def __init__(self):
        self.default_font = "Helvetica"
        self.fonts_path = Path(__file__).parent.parent / "static" / "fonts"
        self.available_fonts = {
            "Inter": {
                "regular": "Inter-Regular.woff2",
                "bold": "Inter-Bold.woff2",
                "italic": "Inter-Italic.woff2",
                "bold_italic": "Inter-BoldItalic.woff2",
            },
            "Roboto": {
                "regular": "Roboto-Regular.ttf",
                "bold": "Roboto-Bold.ttf",
                "italic": "Roboto-Italic.ttf",
                "bold_italic": "Roboto-BoldItalic.ttf",
            },
            "OpenSans": {
                "regular": "OpenSans-Regular.ttf",
                "bold": "OpenSans-Bold.ttf",
                "italic": "OpenSans-Italic.ttf",
                "bold_italic": "OpenSans-BoldItalic.ttf",
            },
            "SourceSansPro": {
                "regular": "SourceSansPro-Regular.ttf",
                "bold": "SourceSansPro-Bold.ttf",
                "italic": "SourceSansPro-It.ttf",
                "bold_italic": "SourceSansPro-BoldIt.ttf",
            },
            "WorkSans": {
                "regular": "WorkSans-Regular.ttf",
                "bold": "WorkSans-Bold.ttf",
                "italic": "WorkSans-Italic.ttf",
                "bold_italic": "WorkSans-BoldItalic.ttf",
            },
            "IBMPlexSans": {
                "regular": "IBMPlexSans-Regular.ttf",
                "bold": "IBMPlexSans-Bold.ttf",
                "italic": "IBMPlexSans-Italic.ttf",
                "bold_italic": "IBMPlexSans-BoldItalic.ttf",
            },
            "MesloLGS": {
                "regular": "MesloLGS-Regular.ttf",
                "bold": "MesloLGS-Bold.ttf",
                "italic": "MesloLGS-Italic.ttf",
                "bold_italic": "MesloLGS-BoldItalic.ttf"
            },
            "SourceCodePro": {
                "regular": "SourceCodePro-Regular.ttf",
                "bold": "SourceCodePro-Bold.ttf",
                "italic": "SourceCodePro-Italic.otf",
                "bold_italic": "SourceCodePro-BoldItalic.otf",
            },
            "Lato": {
                "regular": "Lato-Regular.ttf",
                "bold": "Lato-Bold.ttf",
                "italic": "Lato-Italic.ttf",
                "bold_italic": "Lato-BoldItalic.ttf",
            },
            "NunitoSans": {
                "regular": "NunitoSans-Regular.ttf",
                "bold": "NunitoSans-Bold.ttf",
                "italic": "NunitoSans-Italic.ttf",
                "bold_italic": "NunitoSans-BoldItalic.ttf",
            },
            # Apple SF-style fonts
            "AlbertSans": {
                "regular": "AlbertSans-Regular.ttf",
                "bold": "AlbertSans-Bold.ttf",
                "italic": "AlbertSans-Italic.ttf",
                "bold_italic": "AlbertSans-BoldItalic.ttf",
            },
            "HankenGrotesk": {
                "regular": "HankenGrotesk-Regular.ttf",
                "bold": "HankenGrotesk-Bold.ttf",
                "italic": "HankenGrotesk-Italic.ttf",
                "bold_italic": "HankenGrotesk-BoldItalic.ttf",
            },
            # Helvetica Neue-style fonts
            "Archivo": {
                "regular": "Archivo-Regular.ttf",
                "bold": "Archivo-Bold.ttf",
                "italic": "Archivo-Italic.ttf",
                "bold_italic": "Archivo-BoldItalic.ttf",
            },
            "Manrope": {
                "regular": "Manrope-Regular.ttf",
                "bold": "Manrope-Bold.ttf",
                "italic": "Manrope-Italic.ttf",
                "bold_italic": "Manrope-BoldItalic.ttf",
            },
            "Barlow": {
                "regular": "Barlow-Regular.ttf",
                "bold": "Barlow-Bold.ttf",
                "italic": "Barlow-Italic.ttf",
                "bold_italic": "Barlow-BoldItalic.ttf",
            },
            # Futura-style fonts (geometric sans serif)
            "Jost": {
                "regular": "Jost-Regular.ttf",
                "bold": "Jost-Bold.ttf",
                "italic": "Jost-Italic.ttf",
                "bold_italic": "Jost-BoldItalic.ttf",
            },
            "Spartan": {
                "regular": "LeagueSpartan-Regular.ttf",
                "bold": "LeagueSpartan-Bold.ttf",
                "italic": "LeagueSpartan-Regular.ttf",
                "bold_italic": "LeagueSpartan-Bold.ttf",
            },
            "Formera": {
                "regular": "Formera-Regular.ttf",
                "bold": "Formera-Regular.ttf",
                "italic": "Formera-Regular.ttf",
                "bold_italic": "Formera-Regular.ttf",
            },
        }
        self._fonts_registered = False
        self._monospace_font = None

    def register_fonts(self):
        """Register all fonts with ReportLab"""
        if self._fonts_registered:
            return

        # Register all available fonts
        for font_family, variants in self.available_fonts.items():
            try:
                # Check if all required font files exist
                if all(os.path.exists(self.fonts_path / variants[style])
                      for style in ["regular", "bold", "italic", "bold_italic"]):

                    # Register individual font files
                    pdfmetrics.registerFont(TTFont(font_family, str(self.fonts_path / variants["regular"])))
                    pdfmetrics.registerFont(TTFont(f'{font_family}-Bold', str(self.fonts_path / variants["bold"])))
                    pdfmetrics.registerFont(TTFont(f'{font_family}-Italic', str(self.fonts_path / variants["italic"])))
                    pdfmetrics.registerFont(TTFont(f'{font_family}-BoldItalic', str(self.fonts_path / variants["bold_italic"])))

                    # Create font family
                    pdfmetrics.registerFontFamily(
                        font_family,
                        normal=font_family,
                        bold=f'{font_family}-Bold',
                        italic=f'{font_family}-Italic',
                        boldItalic=f'{font_family}-BoldItalic'
                    )
                    print(f"Registered {font_family} font family")

                    # Set monospace font preference
                    if font_family == "MesloLGS" and not self._monospace_font:
                        self._monospace_font = "MesloLGS"
                    elif font_family == "SourceCodePro" and not self._monospace_font:
                        self._monospace_font = "SourceCodePro"

            except Exception as e:
                print(f"Error registering {font_family} fonts: {e}")
                continue

        # Set fallback monospace font if none were registered
        if not self._monospace_font:
            self._monospace_font = "Courier"
            print("No custom monospace fonts available, using built-in Courier")

        self._fonts_registered = True

    def get_font_face_css(self, font_family: str, for_preview: bool = False) -> str:
        """Return @font-face CSS for the given font family if available."""
        css_rules = []
        files = self.available_fonts.get(font_family)
        if not files:
            return ""

        for style, filename in files.items():
            font_weight = "bold" if "bold" in style else "normal"
            font_style = "italic" if "italic" in style else "normal"

            ext = Path(filename).suffix.lower()
            if ext == ".woff2":
                font_format = "woff2"
            elif ext == ".otf":
                font_format = "opentype"
            else:
                font_format = "truetype"

            # Choose the appropriate path based on context
            if for_preview:
                # For web preview: use webapp public fonts path (accessible via web server)
                font_src = f"/fonts/{filename}"
            else:
                # For PDF generation: use relative path to webapp public fonts from backend
                font_src = f"../markdown2pdf-webapp/public/fonts/{filename}"

            css_rules.append(
                f"@font-face {{ font-family: '{font_family}'; src: url('{font_src}') format('{font_format}'); font-weight: {font_weight}; font-style: {font_style}; }}"
            )

        return "\n".join(css_rules)

    def get_available_fonts(self) -> List[str]:
        """Return list of available font families"""
        # Include the built-in ReportLab fonts and custom fonts
        return ["Inter", "AlbertSans", "HankenGrotesk", "Jost", "Spartan", "Formera", "Archivo", "Manrope", "Barlow", "OpenSans", "Lato", "NunitoSans", "IBMPlexSans", "Roboto", "MesloLGS", "SourceCodePro", "Helvetica", "Times-Roman", "Courier"]

    def get_font_for_style(self, font_family: str, bold: bool = False, italic: bool = False) -> str:
        """Get the appropriate font name for the given style"""
        # Make sure fonts are registered
        if not self._fonts_registered:
            self.register_fonts()

        # Check if the font family is available in our custom fonts
        if font_family in self.available_fonts:
            # Check if all required font files exist
            if all(os.path.exists(self.fonts_path / self.available_fonts[font_family][style])
                  for style in ["regular", "bold", "italic", "bold_italic"]):

                if bold and italic:
                    return f"{font_family}-BoldItalic"
                elif bold:
                    return f"{font_family}-Bold"
                elif italic:
                    return f"{font_family}-Italic"
                else:
                    return font_family

        # Handle built-in fonts for fallback
        if font_family == "Helvetica":
            if bold and italic:
                return "Helvetica-BoldOblique"
            elif bold:
                return "Helvetica-Bold"
            elif italic:
                return "Helvetica-Oblique"
            else:
                return "Helvetica"
        elif font_family == "Times-Roman":
            if bold and italic:
                return "Times-BoldItalic"
            elif bold:
                return "Times-Bold"
            elif italic:
                return "Times-Italic"
            else:
                return "Times-Roman"
        elif font_family == "Courier":
            if bold and italic:
                return "Courier-BoldOblique"
            elif bold:
                return "Courier-Bold"
            elif italic:
                return "Courier-Oblique"
            else:
                return "Courier"
        else:
            # Fallback to Helvetica for unknown fonts
            return "Helvetica"

    def get_monospace_font(self) -> str:
        """Return the monospace font to use for code blocks"""
        # Make sure fonts are registered
        if not self._fonts_registered:
            self.register_fonts()

        return self._monospace_font or "Courier"


# Create a singleton instance
font_service = FontService()
