from typing import List
from app.core.pdf_fetcher import PDFFetcher
from app.core.ocr_processor import OCRProcessor
from app.core.text_line_formatter import TextLineFormatter

class EndpointController:
    """
    Controller for the PDF extraction endpoint.
    Orchestrates the PDF processing pipeline.
    """
    
    def __init__(self):
        """Initialize the controller with its dependencies."""
        self.__pdf_fetcher = PDFFetcher()
        self.__ocr_processor = OCRProcessor()
        self.__text_formatter = TextLineFormatter()
    
    def process_pdf(self, file_url: str) -> List[str]:
        """
        Process a PDF file from URL through the extraction pipeline.
        
        Args:
            file_url: URL of the PDF file to process
            
        Returns:
            List of extracted text lines
            
        Raises:
            Various exceptions from the component classes:
            - PDFInvalidURLError, PDFNetworkError, PDFInvalidContentTypeError, PDFTimeoutError
            - OCRToolNotFoundError, OCRExtractionError, OCRTimeoutError
            - EmptyTextError, TextParsingError
        """
        # Fetch PDF content
        pdf_content = self.__pdf_fetcher.fetch_pdf(file_url)
        
        # Extract text using OCR
        extracted_text = self.__ocr_processor.extract_text(pdf_content)
        
        # Format text into lines
        return self.__text_formatter.format_text(extracted_text) 