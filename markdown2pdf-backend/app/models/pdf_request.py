"""Request models for PDF generation and formatting options."""
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, validator

from app.services.font_service import font_service


class SpacingOption(str, Enum):
    """Available spacing options for rendered content."""

    DEFAULT = "default"
    COMPACT = "compact"
    SPACIOUS = "spacious"


class PDFGenerationRequest(BaseModel):
    """Payload for generating PDFs or previews."""

    markdown: str
    font_family: Optional[str] = "Inter"
    size_level: int = Field(3, ge=1, le=5)
    spacing: SpacingOption = SpacingOption.DEFAULT
    auto_width_tables: bool = True
    filename: Optional[str] = None
    include_index: bool = False
    add_page_breaks: bool = False

    @validator("markdown")
    @classmethod
    def markdown_must_not_be_empty(cls, v):
        """Reject empty markdown submissions."""
        if not v.strip():
            raise ValueError("Markdown cannot be empty")
        return v

    @validator("font_family")
    @classmethod
    def font_family_available(cls, v):
        """Ensure the requested font is available."""
        if v:
            if v not in font_service.get_available_fonts():
                raise ValueError("Unsupported font family")
        return v
