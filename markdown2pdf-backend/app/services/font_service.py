from typing import List, Optional
import os
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class FontService:
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
                "regular": "Archivo[wdth,wght].ttf",
                "bold": "Archivo[wdth,wght].ttf",
                "italic": "Archivo-Italic[wdth,wght].ttf",
                "bold_italic": "Archivo-Italic[wdth,wght].ttf",
            },
            "Manrope": {
                "regular": "Manrope[wght].ttf",
                "bold": "Manrope[wght].ttf",
                "italic": "Manrope[wght].ttf",
                "bold_italic": "Manrope[wght].ttf",
            },
            "Barlow": {
                "regular": "Barlow-Regular.ttf",
                "bold": "Barlow-Bold.ttf",
                "italic": "Barlow-Italic.ttf",
                "bold_italic": "Barlow-BoldItalic.ttf",
            },
            # Futura-style fonts (geometric sans serif)
            "Jost": {
                "regular": "Jost[wght].ttf",
                "bold": "Jost[wght].ttf",
                "italic": "Jost-Italic[wght].ttf",
                "bold_italic": "Jost-Italic[wght].ttf",
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
        
        # First, try to register the MesloLGS font from TTC if available
        try:      
            # If we have individual TTF files for MesloLGS, use them
            if all(os.path.exists(self.fonts_path / self.available_fonts["MesloLGS"][style]) 
                  for style in ["regular", "bold", "italic", "bold_italic"]):
                
                # Register MesloLGS fonts
                pdfmetrics.registerFont(TTFont('MesloLGS', str(self.fonts_path / self.available_fonts["MesloLGS"]["regular"])))
                pdfmetrics.registerFont(TTFont('MesloLGS-Bold', str(self.fonts_path / self.available_fonts["MesloLGS"]["bold"])))
                pdfmetrics.registerFont(TTFont('MesloLGS-Italic', str(self.fonts_path / self.available_fonts["MesloLGS"]["italic"])))
                pdfmetrics.registerFont(TTFont('MesloLGS-BoldItalic', str(self.fonts_path / self.available_fonts["MesloLGS"]["bold_italic"])))
                
                # Create font family
                pdfmetrics.registerFontFamily(
                    'MesloLGS',
                    normal='MesloLGS',
                    bold='MesloLGS-Bold',
                    italic='MesloLGS-Italic',
                    boldItalic='MesloLGS-BoldItalic'
                )
                self._monospace_font = "MesloLGS"
                print("Registered MesloLGS font family")
            
            # Try SourceCodePro as fallback if MesloLGS not available
            elif all(os.path.exists(self.fonts_path / self.available_fonts["SourceCodePro"][style]) 
                  for style in ["regular", "bold", "italic", "bold_italic"]):
                
                # Register SourceCodePro fonts
                pdfmetrics.registerFont(TTFont('SourceCodePro', str(self.fonts_path / self.available_fonts["SourceCodePro"]["regular"])))
                pdfmetrics.registerFont(TTFont('SourceCodePro-Bold', str(self.fonts_path / self.available_fonts["SourceCodePro"]["bold"])))
                pdfmetrics.registerFont(TTFont('SourceCodePro-Italic', str(self.fonts_path / self.available_fonts["SourceCodePro"]["italic"])))
                pdfmetrics.registerFont(TTFont('SourceCodePro-BoldItalic', str(self.fonts_path / self.available_fonts["SourceCodePro"]["bold_italic"])))
                
                # Create font family
                pdfmetrics.registerFontFamily(
                    'SourceCodePro',
                    normal='SourceCodePro',
                    bold='SourceCodePro-Bold',
                    italic='SourceCodePro-Italic',
                    boldItalic='SourceCodePro-BoldItalic'
                )
                self._monospace_font = "SourceCodePro"
                print("Registered SourceCodePro font family as fallback for monospace")
            else:
                print("No monospace font files found, falling back to Courier")
                self._monospace_font = "Courier"
        except Exception as e:
            print(f"Error registering monospace fonts: {e}")
            print("Falling back to built-in Courier font")
            self._monospace_font = "Courier"
            
        self._fonts_registered = True

    def get_font_face_css(self, font_family: str) -> str:
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

            # Use relative path from the backend project root (where run.py is located)
            relative_src = f"app/static/fonts/{filename}"
            css_rules.append(
                f"@font-face {{ font-family: '{font_family}'; src: url('{relative_src}') format('{font_format}'); font-weight: {font_weight}; font-style: {font_style}; }}"
            )

        return "\n".join(css_rules)
    
    def get_available_fonts(self) -> List[str]:
        """Return list of available font families"""
        # Include the built-in ReportLab fonts and custom fonts
        return ["Inter", "AlbertSans", "HankenGrotesk", "Jost", "Spartan", "Formera", "Archivo", "Manrope", "Barlow", "OpenSans", "Lato", "NunitoSans", "IBMPlexSans", "Roboto", "MesloLGS", "SourceCodePro", "Helvetica", "Times-Roman", "Courier"]
    
    def get_font_for_style(self, font_family: str, bold: bool = False, italic: bool = False) -> str:
        """Get the appropriate font name for the given style"""
        # Check if Menlo is requested
        if font_family == "MesloLGS" and self._monospace_font == "MesloLGS":
            if bold and italic:
                return "MesloLGS-BoldItalic" if os.path.exists(self.fonts_path / self.available_fonts["MesloLGS"]["bold_italic"]) else "MesloLGS"
            elif bold:
                return "MesloLGS-Bold" if os.path.exists(self.fonts_path / self.available_fonts["MesloLGS"]["bold"]) else "MesloLGS"
            elif italic:
                return "MesloLGS-Italic" if os.path.exists(self.fonts_path / self.available_fonts["MesloLGS"]["italic"]) else "MesloLGS"
            else:
                return "MesloLGS"
        elif font_family == "SourceCodePro" and self._monospace_font == "SourceCodePro":
            if bold and italic:
                return "SourceCodePro-BoldItalic"
            elif bold:
                return "SourceCodePro-Bold"
            elif italic:
                return "SourceCodePro-Italic"
            else:
                return "SourceCodePro"
        # Handle built-in fonts for fallback
        elif font_family not in ["Helvetica", "Times-Roman", "Courier", "Inter", "Roboto"]:
            font_family = "Helvetica"
            
        # Map to built-in fonts with appropriate styles
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
            return "Helvetica"

    def get_monospace_font(self) -> str:
        """Return the monospace font to use for code blocks"""
        # Make sure fonts are registered
        if not self._fonts_registered:
            self.register_fonts()
            
        return self._monospace_font or "Courier"


# Create a singleton instance
font_service = FontService() 
