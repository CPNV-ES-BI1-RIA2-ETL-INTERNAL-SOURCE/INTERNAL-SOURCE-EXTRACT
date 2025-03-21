"""Custom exceptions for the application."""
from typing import Any, Dict, Optional

class PDFProcessingError(Exception):
    """Base exception for PDF processing errors."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)

# PDF Fetch Errors
class PDFFetchError(PDFProcessingError):
    """Base exception for PDF fetching errors."""
    pass

class PDFInvalidURLError(PDFFetchError):
    """Raised when the PDF URL is invalid."""
    pass

class PDFNetworkError(PDFFetchError):
    """Raised when there's a network error while fetching the PDF."""
    pass

class PDFInvalidContentTypeError(PDFFetchError):
    """Raised when the content type of the response is not PDF."""
    pass

class PDFTimeoutError(PDFFetchError):
    """Raised when the PDF fetch operation times out."""
    pass

# OCR Errors
class OCRError(PDFProcessingError):
    """Base exception for OCR errors."""
    pass

class OCRToolNotFoundError(OCRError):
    """Raised when the OCR tool is not found."""
    pass

class OCRExtractionError(OCRError):
    """Raised when text extraction fails."""
    pass

class OCRTimeoutError(OCRError):
    """Raised when the OCR operation times out."""
    pass

# Text Formatting Errors
class TextFormattingError(PDFProcessingError):
    """Base exception for text formatting errors."""
    pass

class EmptyTextError(TextFormattingError):
    """Raised when the input text is empty."""
    pass

class TextParsingError(TextFormattingError):
    """Raised when there's an error parsing the text."""
    pass 