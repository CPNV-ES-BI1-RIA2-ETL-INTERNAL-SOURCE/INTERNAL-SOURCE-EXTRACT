import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.endpointController import api_router

client = TestClient(api_router)

TEST_PDF_PATH = "./tests/lausanne_24-12-12.pdf"

# TODO Data and logic have to be split.
EXPECTED_JSON = [
    'Gare de Lausanne',
    'État au 12/12/24',
    'Heure de départ   Ligne   Destination   Vias                                                                                                                               Voie',
    '0 02              R       Palézieux     Pully-Nord, La Conversion, Grandvaux, Puidoux, Moreillon, Palézieux                                                                1',
    '0 14              IC 5    Biel/Bienne   Yverdon-les-Bains, Neuchâtel, Biel/Bienne                                                                                          5',
    '0 17              R       Vallorbe      Prilly-Malley, Renens VD, Bussigny, Vufflens-la-Ville, Cossonay-Penthalaz, La Sarraz, Arnex, Croy-Romainmôtier, Le Day, Vallorbe   8',
    '0 25              IR      Sion          Vevey, Montreux, Aigle, Bex, St-Maurice, Martigny, Sion                                                                            3',
    '0 25              RE      Genève        Renens VD, Morges, Allaman, Rolle, Gland, Nyon, Coppet, Genève                                                                     7'
]


@pytest.fixture
def mock_pdf_fetcher():
    with patch("app.pdfFetcher.PDFFetcher.fetch_pdf") as mock_fetch_pdf:
        with open(TEST_PDF_PATH, "rb") as f:
            mock_fetch_pdf.return_value = f.read()
        yield mock_fetch_pdf


def test_can_extract_data_and_send_json(mock_pdf_fetcher):
    response = client.get("/api/v1/extract/?url=https%3A%2F%2Fs3.eu-south-1.amazonaws.com%2Fdev.data.generator.cld.education%2F2025-01-17%2F8504200.pdf%3FX-Amz-Algorithm%3DAWS4-HMAC-SHA256%26X-Amz-Credential%3DAKIA2KFJKL4O35LD5P3Z%252F20250122%252Feu-south-1%252Fs3%252Faws4_request%26X-Amz-Date%3D20250122T093428Z%26X-Amz-Expires%3D3600%26X-Amz-SignedHeaders%3Dhost%26X-Amz-Signature%3D199ad4b3a0387e8a86199f3494695f9a12d215ec3a058fa2a845d6915b8a725a")

    assert response.status_code == 200
    assert response.json() == EXPECTED_JSON


def test_pdf_not_existing(mock_pdf_fetcher):
    mock_pdf_fetcher.side_effect = ValueError("The pdf is not existing")

    response = client.get("/api/v1/extract/?url=https%3A%2F%2Fs3.eu-south-1.amazonaws.com%2Fdev.data.generator.cld.education%2F2025-01-17%2F8504200.pdf%3FX-Amz-Algorithm%3DAWS4-HMAC-SHA256%26X-Amz-Credential%3DAKIA2KFJKL4O35LD5P3Z%252F20250122%252Feu-south-1%252Fs3%252Faws4_request%26X-Amz-Date%3D20250122T093428Z%26X-Amz-Expires%3D3600%26X-Amz-SignedHeaders%3Dhost%26X-Amz-Signature%3D199ad4b3a0387e8a86199f3494695f9a12d215ec3a058fa2a845d6915b8a725a")

    # TODO You test the extraction of a pdf. Why have API-specific error codes ?
    assert response.status_code == 400
    assert response.json() == {"detail": "The pdf is not existing"}


def test_invalid_pdf(mock_pdf_fetcher):
    mock_pdf_fetcher.side_effect = ValueError("Fetched content is not a PDF.")

    response = client.get("/api/v1/extract/?url=https%3A%2F%2Fs3.eu-south-1.amazonaws.com%2Fdev.data.generator.cld.education%2F2025-01-17%2F8504200.pdf%3FX-Amz-Algorithm%3DAWS4-HMAC-SHA256%26X-Amz-Credential%3DAKIA2KFJKL4O35LD5P3Z%252F20250122%252Feu-south-1%252Fs3%252Faws4_request%26X-Amz-Date%3D20250122T093428Z%26X-Amz-Expires%3D3600%26X-Amz-SignedHeaders%3Dhost%26X-Amz-Signature%3D199ad4b3a0387e8a86199f3494695f9a12d215ec3a058fa2a845d6915b8a725a")

    assert response.status_code == 400
    assert response.json() == {"detail": "Fetched content is not a PDF."}