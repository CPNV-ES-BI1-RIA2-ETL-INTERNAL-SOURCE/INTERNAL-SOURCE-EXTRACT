import pytest
from unittest.mock import patch, Mock
from app.core.ocr_processor import OCRProcessor
from app.exceptions import OCRToolNotFoundError, OCRExtractionError, OCRTimeoutError
import subprocess

class TestOCRProcessor:
    @pytest.fixture
    def ocr_processor(self):
        return OCRProcessor()

    def test_extract_text_from_valid_content(self, ocr_processor, sample_pdf_content):
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(
                stdout="Gare de Lausanne\nDestination\nVoie",
                stderr="",
                returncode=0
            )
            result = ocr_processor.extract_text(sample_pdf_content)
            assert "Gare de Lausanne" in result
            assert "Destination" in result

    def test_extract_text_handles_empty_content(self, ocr_processor):
        with pytest.raises(OCRExtractionError) as exc_info:
            ocr_processor.extract_text(b"")
        assert "Empty PDF data" in str(exc_info.value)

    def test_extract_text_handles_subprocess_error(self, ocr_processor, sample_pdf_content):
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                returncode=1,
                cmd="pdftotext",
                stderr="Syntax Error: Not a PDF file"
            )
            with pytest.raises(OCRExtractionError) as exc_info:
                ocr_processor.extract_text(sample_pdf_content)
            assert "Text extraction failed" in str(exc_info.value)
            assert "return_code" in exc_info.value.details

    def test_pdftotext_not_found(self, ocr_processor):
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = FileNotFoundError()
            with pytest.raises(OCRToolNotFoundError) as exc_info:
                ocr_processor.extract_text(b"some content")
            assert "OCR tool not found" in str(exc_info.value)
            assert "tool" in exc_info.value.details

    def test_extract_text_timeout(self, ocr_processor, sample_pdf_content):
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired(cmd="pdftotext", timeout=30)
            with pytest.raises(OCRTimeoutError) as exc_info:
                ocr_processor.extract_text(sample_pdf_content)
            assert "OCR operation timed out" in str(exc_info.value)
            assert "timeout" in exc_info.value.details

    def test_extract_text_preserves_structure(self, ocr_processor, sample_pdf_content, expected_json_data):
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(
                stdout="\n".join(expected_json_data),
                stderr="",
                returncode=0
            )
            result = ocr_processor.extract_text(sample_pdf_content)
            lines = result.split('\n')
            
            # Check key structural elements
            assert any("Heure de départ" in line for line in lines)
            assert any("Destination" in line for line in lines)
            assert any("Voie" in line for line in lines) 