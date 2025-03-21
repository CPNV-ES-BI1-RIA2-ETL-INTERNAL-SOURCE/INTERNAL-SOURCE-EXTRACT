import pytest
import json
from pathlib import Path

# Constants
TEST_DATA_DIR = Path(__file__).parent / "test_data"
TEST_PDF_PATH = TEST_DATA_DIR / "lausanne_24-12-12.pdf"
TEST_FIXTURES_PATH = TEST_DATA_DIR / "fixtures"

@pytest.fixture
def test_pdf_path():
    return TEST_PDF_PATH

@pytest.fixture
def expected_json_data():
    with open(TEST_FIXTURES_PATH / "expected_output.json") as f:
        return json.load(f)

@pytest.fixture
def sample_pdf_content():
    with open(TEST_PDF_PATH, "rb") as f:
        return f.read()

@pytest.fixture
def invalid_pdf_content():
    return b"This is not a PDF file content" 