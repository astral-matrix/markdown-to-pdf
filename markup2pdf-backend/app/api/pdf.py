from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
import io

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
        
        # Return the PDF as a streaming response
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=document.pdf"
            }
        )
    except Exception as e:
        # Log the error in a real application
        print(f"Error generating PDF: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate PDF"
        ) 