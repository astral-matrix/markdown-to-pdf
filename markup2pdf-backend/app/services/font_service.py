from typing import List
import os
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class FontService:
    def __init__(self):
        self.default_font = "Inter"
        self.available_fonts = {
            "Inter": {
                "regular": "Inter-Regular.ttf",
                "bold": "Inter-Bold.ttf",
                "italic": "Inter-Italic.ttf",
                "bold_italic": "Inter-BoldItalic.ttf",
            },
            "Roboto": {
                "regular": "Roboto-Regular.ttf",
                "bold": "Roboto-Bold.ttf",
                "italic": "Roboto-Italic.ttf",
                "bold_italic": "Roboto-BoldItalic.ttf",
            },
            "Source Code Pro": {
                "regular": "SourceCodePro-Regular.ttf",
                "bold": "SourceCodePro-Bold.ttf",
                "italic": "SourceCodePro-Italic.ttf",
                "bold_italic": "SourceCodePro-BoldItalic.ttf",
            }
        }
        self._fonts_registered = False
        
    def register_fonts(self):
        """Register all fonts with ReportLab"""
        if self._fonts_registered:
            return
            
        fonts_dir = Path(__file__).parent.parent / "static" / "fonts"
        os.makedirs(fonts_dir, exist_ok=True)
        
        # TODO: In production, ensure all font files exist
        # For now, we'll assume they're available
        
        for font_family, variants in self.available_fonts.items():
            for style, filename in variants.items():
                font_path = fonts_dir / filename
                if style == "regular":
                    pdfmetrics.registerFont(TTFont(font_family, str(font_path)))
                else:
                    style_name = f"{font_family}-{style.replace('_', '')}"
                    pdfmetrics.registerFont(TTFont(style_name, str(font_path)))
                    
        self._fonts_registered = True
    
    def get_available_fonts(self) -> List[str]:
        """Return list of available font families"""
        return list(self.available_fonts.keys())
    
    def get_font_for_style(self, font_family: str, bold: bool = False, italic: bool = False) -> str:
        """Get the appropriate font name for the given style"""
        if font_family not in self.available_fonts:
            font_family = self.default_font
            
        if bold and italic:
            return f"{font_family}-bolditalic"
        elif bold:
            return f"{font_family}-bold"
        elif italic:
            return f"{font_family}-italic"
        else:
            return font_family


# Create a singleton instance
font_service = FontService() 