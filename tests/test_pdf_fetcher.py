import pytest
from unittest.mock import patch, Mock
from app.core.pdf_fetcher import PDFFetcher
from app.exceptions import PDFInvalidURLError, PDFNetworkError, PDFInvalidContentTypeError, PDFTimeoutError
import requests

class TestPDFFetcher:
    @pytest.fixture
    def pdf_fetcher(self):
        with patch.dict('os.environ', {'PDF_API_BASE_URL': 'http://example.com'}):
            return PDFFetcher()

    def test_fetch_valid_pdf(self, pdf_fetcher, sample_pdf_content):
        with patch("app.core.pdf_fetcher.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.content = sample_pdf_content
            mock_response.status_code = 200
            mock_response.headers = {"Content-Type": "application/pdf"}
            mock_get.return_value = mock_response

            result = pdf_fetcher.fetch_pdf("http://example.com/test.pdf")
            assert result == sample_pdf_content

    def test_fetch_invalid_url(self, pdf_fetcher):
        with pytest.raises(PDFInvalidURLError) as exc_info:
            pdf_fetcher.fetch_pdf("not-a-valid-url")
        assert "Invalid PDF URL" in str(exc_info.value)
        assert "url" in exc_info.value.details

    def test_fetch_network_error(self, pdf_fetcher):
        with patch("app.core.pdf_fetcher.requests.get") as mock_get:
            mock_get.side_effect = requests.RequestException("Network error")
            
            with pytest.raises(PDFNetworkError) as exc_info:
                pdf_fetcher.fetch_pdf("http://example.com/test.pdf")
            assert "Failed to fetch PDF" in str(exc_info.value)
            assert "url" in exc_info.value.details

    def test_fetch_non_pdf_content(self, pdf_fetcher, invalid_pdf_content):
        with patch("app.core.pdf_fetcher.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.content = invalid_pdf_content
            mock_response.status_code = 200
            mock_response.headers = {"Content-Type": "text/plain"}
            mock_get.return_value = mock_response

            with pytest.raises(PDFInvalidContentTypeError) as exc_info:
                pdf_fetcher.fetch_pdf("http://example.com/not-pdf.txt")
            assert "Invalid content type" in str(exc_info.value)
            assert "content_type" in exc_info.value.details

    def test_fetch_server_error(self, pdf_fetcher):
        with patch("app.core.pdf_fetcher.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.raise_for_status.side_effect = requests.HTTPError("500 Server Error")
            mock_get.return_value = mock_response

            with pytest.raises(PDFNetworkError) as exc_info:
                pdf_fetcher.fetch_pdf("http://example.com/test.pdf")
            assert "Failed to fetch PDF" in str(exc_info.value)

    def test_fetch_timeout(self, pdf_fetcher):
        with patch("app.core.pdf_fetcher.requests.get") as mock_get:
            mock_get.side_effect = requests.Timeout("Request timed out")
            
            with pytest.raises(PDFTimeoutError) as exc_info:
                pdf_fetcher.fetch_pdf("http://example.com/test.pdf")
            assert "PDF fetch operation timed out" in str(exc_info.value)
            assert "timeout" in exc_info.value.details

    def test_default_base_url(self):
        with patch.dict('os.environ', {'PDF_API_BASE_URL': ''}):
            fetcher = PDFFetcher()
            assert fetcher.settings.pdf_api_base_url == "http://localhost:8000" 