from fastapi import APIRouter
from typing import List

from app.services import font_service

router = APIRouter()


@router.get("/fonts", response_model=List[str])
async def get_available_fonts():
    """
    Get a list of available font families for PDF generation.
    """
    return font_service.get_available_fonts() 