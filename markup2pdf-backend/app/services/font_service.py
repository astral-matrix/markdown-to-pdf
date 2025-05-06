from typing import List
import os
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class FontService:
    def __init__(self):
        self.default_font = "Helvetica"
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
            "SourceCodePro": {
                "regular": "SourceCodePro-Regular.ttf",
                "bold": "SourceCodePro-Bold.ttf",
                "italic": "SourceCodePro-Italic.otf",
                "bold_italic": "SourceCodePro-BoldItalic.otf",
            }
        }
        self._fonts_registered = False
        
    def register_fonts(self):
        """Register all fonts with ReportLab"""
        if self._fonts_registered:
            return
            
        # Just use built-in fonts for now since we're having issues with font conversion
        # ReportLab has built-in Helvetica, Times, Courier and Symbol
        self._fonts_registered = True
    
    def get_available_fonts(self) -> List[str]:
        """Return list of available font families"""
        # Include the built-in ReportLab fonts
        return ["Helvetica", "Times-Roman", "Courier"]
    
    def get_font_for_style(self, font_family: str, bold: bool = False, italic: bool = False) -> str:
        """Get the appropriate font name for the given style"""
        # Only use built-in fonts to avoid conversion issues
        if font_family not in ["Helvetica", "Times-Roman", "Courier"]:
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


# Create a singleton instance
font_service = FontService() 