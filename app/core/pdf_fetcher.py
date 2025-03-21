import requests
from pydantic import HttpUrl
from app.config import get_settings
from app.exceptions import PDFInvalidURLError, PDFNetworkError, PDFInvalidContentTypeError, PDFTimeoutError

class PDFFetcher:
    """Fetch PDF files from URLs."""
    
    def __init__(self):
        """Initialize the PDF fetcher."""
        self.settings = get_settings()

    def fetch_pdf(self, url: str) -> bytes:
        """
        Fetch and validate a PDF file from a URL.
        
        Args:
            url: URL of the PDF file to fetch
            
        Returns:
            Raw PDF content as bytes
            
        Raises:
            PDFInvalidURLError: If the URL is invalid
            PDFNetworkError: If there's a network error while fetching the PDF
            PDFInvalidContentTypeError: If the content type is not PDF
            PDFTimeoutError: If the fetch operation times out
        """
        # Validate URL
        try:
            HttpUrl(url)
        except ValueError as e:
            raise PDFInvalidURLError(
                message="Invalid PDF URL",
                details={"url": url, "error": str(e)}
            )
        
        # Fetch content with timeout
        try:
            response = requests.get(url, timeout=10)  # 10 seconds timeout
            response.raise_for_status()
        except requests.Timeout as e:
            raise PDFTimeoutError(
                message="PDF fetch operation timed out",
                details={"url": url, "timeout": 10, "error": str(e)}
            )
        except requests.RequestException as e:
            raise PDFNetworkError(
                message="Failed to fetch PDF",
                details={"url": url, "error": str(e)}
            )
        
        # Validate content type
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("application/pdf"):
            raise PDFInvalidContentTypeError(
                message="Invalid content type",
                details={
                    "url": url,
                    "content_type": content_type,
                    "expected": "application/pdf"
                }
            )
            
        return response.content 