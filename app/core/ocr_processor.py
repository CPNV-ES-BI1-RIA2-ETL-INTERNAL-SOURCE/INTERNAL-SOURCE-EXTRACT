import subprocess
import tempfile
from app.exceptions import OCRToolNotFoundError, OCRExtractionError, OCRTimeoutError

class OCRProcessor:
    """Extract text from PDF files using OCR."""
    
    def extract_text(self, pdf_data: bytes) -> str:
        """
        Extract text from PDF data using pdftotext.
        
        Args:
            pdf_data: Raw PDF content as bytes
            
        Returns:
            Extracted text as string
            
        Raises:
            OCRToolNotFoundError: If the OCR tool is not found
            OCRExtractionError: If text extraction fails
            OCRTimeoutError: If the OCR operation times out
        """
        if not pdf_data:
            raise OCRExtractionError(
                message="Empty PDF data",
                details={"pdf_data_length": 0}
            )
            
        with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_pdf:
            # Save PDF to temp file
            temp_pdf.write(pdf_data)
            temp_pdf.flush()
            
            try:
                # Run OCR with timeout
                result = subprocess.run(
                    ["pdftotext", "-layout", temp_pdf.name, "-"],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=30  # 30 seconds timeout
                )
            except FileNotFoundError:
                raise OCRToolNotFoundError(
                    message="OCR tool not found",
                    details={"tool": "pdftotext"}
                )
            except subprocess.TimeoutExpired as e:
                raise OCRTimeoutError(
                    message="OCR operation timed out",
                    details={"timeout": 30, "error": str(e)}
                )
            except subprocess.CalledProcessError as e:
                raise OCRExtractionError(
                    message="Text extraction failed",
                    details={
                        "command": e.cmd,
                        "return_code": e.returncode,
                        "stderr": e.stderr
                    }
                )
            
            return result.stdout.strip() 