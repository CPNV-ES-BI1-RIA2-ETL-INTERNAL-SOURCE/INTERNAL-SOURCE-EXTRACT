"""API schemas."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, HttpUrl

class PDFResponse(BaseModel):
    """Response model for PDF text extraction."""
    data: List[str]

class ErrorDetail(BaseModel):
    """Detailed error information."""
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    """Standard error response."""
    error: ErrorDetail 