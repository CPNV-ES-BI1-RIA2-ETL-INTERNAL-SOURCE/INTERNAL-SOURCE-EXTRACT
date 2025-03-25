from fastapi import APIRouter, HTTPException, Query
from app.core.endpoint_controller import EndpointController
from app.exceptions import (
    PDFInvalidURLError, PDFNetworkError, PDFInvalidContentTypeError, PDFTimeoutError,
    OCRToolNotFoundError, OCRExtractionError, OCRTimeoutError,
    EmptyTextError, TextParsingError
)
from app.schemas import PDFResponse, ErrorResponse, ErrorDetail
from typing import Dict, Any, Type, Optional

router = APIRouter(
    prefix="/api/v1",
    tags=["PDF Processing"]
)

# Exception mapping configuration
EXCEPTION_HANDLERS = {
    # 400 Bad Request errors
    PDFInvalidURLError: (400, "PDF_INVALID_URL_ERROR"),
    PDFInvalidContentTypeError: (400, "PDF_INVALID_CONTENT_TYPE_ERROR"),
    PDFNetworkError: (400, "PDF_NETWORK_ERROR"),
    
    # 504 Gateway Timeout errors
    PDFTimeoutError: (504, "PDF_TIMEOUT_ERROR"),
    OCRTimeoutError: (504, "OCR_TIMEOUT_ERROR"),
    
    # 500 Internal Server Error - OCR errors
    OCRToolNotFoundError: (500, "OCR_TOOL_NOT_FOUND_ERROR"),
    OCRExtractionError: (500, "OCR_EXTRACTION_ERROR"),
    
    # 500 Internal Server Error - Text formatting errors
    EmptyTextError: (500, "EMPTY_TEXT_ERROR"),
    TextParsingError: (500, "TEXT_PARSING_ERROR"),
}

def handle_exception(exception: Exception) -> HTTPException:
    """
    Convert application exceptions to appropriate HTTPExceptions.
    
    Args:
        exception: The exception to handle
        
    Returns:
        HTTPException with appropriate status code and details
    """
    # Find the exception type in our mapping
    for exc_type, (status_code, error_code) in EXCEPTION_HANDLERS.items():
        if isinstance(exception, exc_type):
            return HTTPException(
                status_code=status_code,
                detail=ErrorDetail(
                    code=error_code,
                    message=str(exception.message),
                    details=exception.details
                ).model_dump()
            )
    
    # Default case for unhandled exceptions
    return HTTPException(
        status_code=500,
        detail=ErrorDetail(
            code="INTERNAL_SERVER_ERROR",
            message=f"An unexpected error occurred: {str(exception)}",
            details={"error": str(exception)}
        ).model_dump()
    )

@router.get(
    "/documents/extract-text",
    response_model=PDFResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Processing error"},
        504: {"model": ErrorResponse, "description": "Timeout error"}
    }
)
async def extract_document_text(
    file: str = Query(..., description="URL of the PDF file to process")
) -> PDFResponse:
    """
    Extract text from a PDF document.
    
    Args:
        file: URL of the PDF file to process
        
    Returns:
        PDFResponse containing extracted text lines
        
    Raises:
        HTTPException: If document processing fails
    """
    try:
        controller = EndpointController()
        text_lines = controller.process_pdf(file)
        return PDFResponse.model_validate(text_lines)
    except Exception as e:
        raise handle_exception(e) 