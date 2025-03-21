from typing import List
from app.exceptions import EmptyTextError, TextParsingError

class TextLineFormatter:
    """Format extracted text into a list of non-empty lines."""
    
    def format_text(self, text: str) -> List[str]:
        """
        Format extracted text into a list of non-empty lines.
        
        Args:
            text: Raw text to format
            
        Returns:
            List of non-empty text lines
            
        Raises:
            EmptyTextError: If the input text is empty
            TextParsingError: If there's an error parsing the text
        """
        if not text:
            raise EmptyTextError(
                message="Empty text input",
                details={"text": text}
            )
            
        # Split text into lines and filter out empty ones
        lines = [line.strip() for line in text.splitlines()]
        non_empty_lines = [line for line in lines if line]
        
        if not non_empty_lines:
            raise EmptyTextError(
                message="No non-empty lines found in text",
                details={"text": text, "line_count": len(lines)}
            )
            
        return non_empty_lines 