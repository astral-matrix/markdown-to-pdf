from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from app.api import api_router

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Markup2PDF API",
    description="API for converting Markdown to PDF with custom styling",
    version="1.0.0",
)

# Configure CORS
origins = [
    "http://localhost:3000",  # Next.js development server
    "http://localhost:8000",  # For local testing
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"} 