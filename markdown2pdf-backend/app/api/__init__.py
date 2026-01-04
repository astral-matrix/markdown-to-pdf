"""API router wiring."""
from fastapi import APIRouter

from app.api.pdf import router as pdf_router
from app.api.fonts import router as fonts_router

api_router = APIRouter()
api_router.include_router(pdf_router, tags=["pdf"])
api_router.include_router(fonts_router, tags=["fonts"])
