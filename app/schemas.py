"""API schemas."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, RootModel


class PDFResponse(RootModel):
    """Response model for PDF text extraction."""
    root: List[str]

class ErrorDetail(BaseModel):
    """Detailed error information."""
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    """Standard error response."""
    error: ErrorDetail