import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from weasyprint import HTML

from app.models import PDFGenerationRequest, SpacingOption
from app.services.font_service import font_service
from app.services.markdown_service import markdown_service


class PDFService:
    def __init__(self):
        self.page_size = A4
        self.margin = 25 * 2.83465  # 25mm in points (1mm = 2.83465pt)
        
        # Size level to base font size mapping
        self.size_level_mapping = {
            1: 8,    # Smallest
            2: 10,
            3: 12,   # Default
            4: 14,
            5: 18,   # Largest
        }
        
        # Spacing option to line spacing mapping
        self.spacing_mapping = {
            SpacingOption.COMPACT: 1.1,
            SpacingOption.DEFAULT: 1.4,
            SpacingOption.SPACIOUS: 1.8,
        }
    
    def _get_base_font_size(self, size_level: int) -> int:
        """Get base font size from size level"""
        return self.size_level_mapping.get(size_level, self.size_level_mapping[3])
    
    def _get_line_spacing(self, spacing: SpacingOption) -> float:
        """Get line spacing multiplier from spacing option"""
        return self.spacing_mapping.get(spacing, self.spacing_mapping[SpacingOption.DEFAULT])
    
    def _setup_styles(self, font_family: str, size_level: int, spacing: SpacingOption):
        """Setup paragraph styles based on user preferences"""
        # Register fonts with ReportLab if not already done
        font_service.register_fonts()
        
        # Get base font size and line spacing
        base_size = self._get_base_font_size(size_level)
        line_spacing = self._get_line_spacing(spacing)
        
        # Create styles dictionary
        styles = getSampleStyleSheet()
        
        # Normal paragraphs
        styles['Normal'].fontName = font_service.get_font_for_style(font_family)
        styles['Normal'].fontSize = base_size
        styles['Normal'].leading = base_size * line_spacing
        styles['Normal'].alignment = 4  # Justified
        
        # Headings
        styles['Heading1'].fontName = font_service.get_font_for_style(font_family, bold=True)
        styles['Heading1'].fontSize = base_size * 2.0
        styles['Heading1'].leading = base_size * 2.0 * line_spacing
        
        styles['Heading2'].fontName = font_service.get_font_for_style(font_family, bold=True)
        styles['Heading2'].fontSize = base_size * 1.5
        styles['Heading2'].leading = base_size * 1.5 * line_spacing
        
        styles['Heading3'].fontName = font_service.get_font_for_style(font_family, bold=True)
        styles['Heading3'].fontSize = base_size * 1.25
        styles['Heading3'].leading = base_size * 1.25 * line_spacing
        
        # Code style
        code_style = ParagraphStyle(
            'Code',
            fontName='Source Code Pro',
            fontSize=base_size - 1,
            leading=(base_size - 1) * line_spacing,
            backColor=colors.lightgrey,
            borderPadding=5,
        )
        styles.add(code_style)
        
        return styles
        
    def generate_pdf_reportlab(self, request: PDFGenerationRequest) -> bytes:
        """Generate PDF using ReportLab (to be implemented)"""
        # TODO: Implement full ReportLab PDF generation
        # For now, we'll use WeasyPrint as a fallback
        return self.generate_pdf_weasyprint(request)
    
    def generate_pdf_weasyprint(self, request: PDFGenerationRequest) -> bytes:
        """Generate PDF using WeasyPrint as a fallback"""
        # Convert markdown to HTML
        html_content = markdown_service.convert_to_html(request.markup)
        
        # Create a BytesIO object to store the PDF
        pdf_buffer = io.BytesIO()
        
        # Use WeasyPrint to generate PDF
        HTML(string=html_content).write_pdf(
            pdf_buffer,
            presentational_hints=True,
        )
        
        # Get the PDF bytes
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()
        
    def generate_pdf(self, request: PDFGenerationRequest) -> bytes:
        """
        Generate PDF from markdown with user-specified styling options.
        Will attempt to use ReportLab first, then fall back to WeasyPrint if needed.
        """
        try:
            # Try ReportLab first (golden implementation)
            return self.generate_pdf_reportlab(request)
        except Exception as e:
            # Log the error in a real application
            print(f"ReportLab PDF generation failed: {e}")
            # Fall back to WeasyPrint
            return self.generate_pdf_weasyprint(request)


# Create a singleton instance
pdf_service = PDFService() 