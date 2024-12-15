import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.endpointController import api_router

client = TestClient(api_router)

TEST_PDF_PATH = "./tests/lausanne_24-12-12.pdf"

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
    response = client.get("/process-pdf/?train_station=Yverdon-les-bains&day=2024-12-09")

    assert response.status_code == 200
    assert response.json() == EXPECTED_JSON


def test_pdf_not_existing(mock_pdf_fetcher):
    mock_pdf_fetcher.side_effect = ValueError("The pdf is not existing")

    response = client.get("/process-pdf/?train_station=Lausanne&day=2024-12-10")

    assert response.status_code == 400
    assert response.json() == {"detail": "The pdf is not existing"}


def test_invalid_pdf(mock_pdf_fetcher):
    mock_pdf_fetcher.side_effect = ValueError("Fetched content is not a PDF.")

    response = client.get("/process-pdf/?train_station=Yverdon-les-bains&day=2024-12-09")

    assert response.status_code == 400
    assert response.json() == {"detail": "Fetched content is not a PDF."}