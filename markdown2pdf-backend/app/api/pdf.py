"""PDF generation and preview endpoints."""
# pylint: disable=duplicate-code
import io

from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse

from app.models import PDFGenerationRequest
from app.services import pdf_service

router = APIRouter()


@router.post("/generate-pdf")
async def generate_pdf(request: PDFGenerationRequest):
    """
    Generate a PDF from markdown content with specified styling options.
    """
    try:
        # Generate PDF
        pdf_bytes = pdf_service.generate_pdf(request)

        # Use provided filename or default to "document"
        filename = "document.pdf"
        if request.filename:
            filename = f"{request.filename}.pdf"

        # Return the PDF as a streaming response
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except Exception as e:
        # Log the error in a real application
        print(f"Error generating PDF: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate PDF"
        ) from e


@router.post("/generate-pdf-preview")
async def generate_pdf_preview(request: PDFGenerationRequest):
    """
    Generate HTML preview of the PDF content without creating an actual PDF.
    Returns the styled HTML that would be used for PDF generation.
    """
    try:
        # Generate HTML preview
        html_content = pdf_service.generate_pdf_preview(request)

        # Return the HTML as plain text response
        return Response(
            content=html_content,
            media_type="text/html",
            headers={
                "Content-Type": "text/html; charset=utf-8"
            }
        )
    except Exception as e:
        # Log the error in a real application
        print(f"Error generating PDF preview: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate PDF preview"
        ) from e
