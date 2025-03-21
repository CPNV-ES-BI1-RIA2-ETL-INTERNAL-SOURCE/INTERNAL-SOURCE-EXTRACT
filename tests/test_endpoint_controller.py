from typing import Dict, Any
import pytest
from fastapi.testclient import TestClient
from fastapi import status
from unittest.mock import Mock, patch

from app.core.endpoint_controller import EndpointController
from app.api.router import router as api_router
from app.exceptions import (
    PDFFetchError, OCRError, TextFormattingError
)

class TestExtractEndpoint:
    """Test suite for the PDF extraction endpoint."""
    
    @pytest.fixture
    def test_client(self) -> TestClient:
        """Create a test client for the FastAPI application."""
        return TestClient(api_router, raise_server_exceptions=False)

    @pytest.fixture
    def mocked_components(self) -> Dict[str, Mock]:
        """Set up mock objects for all dependencies with default successful behavior."""
        with patch("app.core.endpoint_controller.PDFFetcher") as mock_pdf_fetcher_class, \
             patch("app.core.endpoint_controller.OCRProcessor") as mock_ocr_processor_class, \
             patch("app.core.endpoint_controller.TextLineFormatter") as mock_text_formatter_class:
            
            # Create mock instances
            mock_pdf_fetcher = Mock()
            mock_ocr_processor = Mock()
            mock_text_formatter = Mock()
            
            # Configure class mocks to return instance mocks
            mock_pdf_fetcher_class.return_value = mock_pdf_fetcher
            mock_ocr_processor_class.return_value = mock_ocr_processor
            mock_text_formatter_class.return_value = mock_text_formatter
            
            # Configure default successful behavior
            mock_pdf_fetcher.fetch_pdf.return_value = b"Sample PDF content"
            mock_ocr_processor.extract_text.return_value = "Sample extracted text"
            mock_text_formatter.format_text.return_value = ["Line1", "Line2"]
            
            yield {
                "pdf_fetcher": mock_pdf_fetcher,
                "ocr_processor": mock_ocr_processor,
                "text_formatter": mock_text_formatter
            }

    @pytest.fixture
    def sample_url(self) -> str:
        """Provide a sample URL for testing."""
        return "http://example.com/test.pdf"

    def test_extract_success(
        self,
        test_client: TestClient,
        mocked_components: Dict[str, Mock],
        sample_url: str
    ):
        """Test successful PDF extraction."""
        # Setup test data
        test_data = ["Line1", "Line2"]
        mocked_components["text_formatter"].format_text.return_value = test_data

        # Execute request
        response = test_client.get("/api/v1/documents/extract-text", params={"file": sample_url})
        
        # Verify response
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"data": test_data}

    def test_extract_validation_errors(self, test_client):
        """Test input validation error scenarios."""
        response = test_client.get("/api/v1/documents/extract-text", params=None)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    @pytest.mark.parametrize("error_scenario", [
        {
            "component": "pdf_fetcher",
            "exception": PDFFetchError("Failed to fetch PDF"),
            "expected_status": status.HTTP_500_INTERNAL_SERVER_ERROR
        },
        {
            "component": "ocr_processor",
            "exception": OCRError("Failed to extract text from PDF"),
            "expected_status": status.HTTP_500_INTERNAL_SERVER_ERROR
        },
        {
            "component": "text_formatter",
            "exception": TextFormattingError("Text formatting failed"),
            "expected_status": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    ])
    def test_extract_component_errors(
        self,
        test_client: TestClient,
        mocked_components: Dict[str, Mock],
        sample_url: str,
        error_scenario: Dict[str, Any]
    ):
        """Test error handling for various component failures."""
        # Setup mock to simulate failure
        if error_scenario["component"] == "pdf_fetcher":
            mocked_components[error_scenario["component"]].fetch_pdf.side_effect = error_scenario["exception"]
        elif error_scenario["component"] == "ocr_processor":
            mocked_components[error_scenario["component"]].extract_text.side_effect = error_scenario["exception"]
        elif error_scenario["component"] == "text_formatter":
            mocked_components[error_scenario["component"]].format_text.side_effect = error_scenario["exception"]
        
        # Execute request
        response = test_client.get("/api/v1/documents/extract-text", params={"file": sample_url})
        
        # Verify response status code
        assert response.status_code == error_scenario["expected_status"]

    def test_component_initialization(
        self,
        test_client: TestClient,
        mocked_components: Dict[str, Mock],
        sample_url: str
    ):
        """Test that all components are properly initialized and called."""
        test_client.get("/api/v1/documents/extract-text", params={"file": sample_url})
        
        # Verify that all components were called
        mocked_components["pdf_fetcher"].fetch_pdf.assert_called_once_with(sample_url)
        mocked_components["ocr_processor"].extract_text.assert_called_once()
        mocked_components["text_formatter"].format_text.assert_called_once() 