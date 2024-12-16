import os
from datetime import date

import requests
from dotenv import load_dotenv

load_dotenv()


class PDFFetcher:
    PDF_CONTENT_TYPE = "application/pdf"

    def __init__(self):
        self.base_url = os.getenv("PDF_API_BASE_URL", "").strip()
        if not self.base_url:
            raise ValueError("Environment variable 'PDF_API_BASE_URL' is not set or empty.")

    def fetch_pdf(self, country: str, train_station: str, day: date) -> str:
        params = {
            "date": day.strftime("%m/%d/%Y"),
        }

        url = self.base_url.format(country=country, train_station=train_station)

        try:
            response = requests.get(url, params=params, headers={"Accept": self.PDF_CONTENT_TYPE})
            response.raise_for_status()

            content_type = response.headers.get("Content-Type")
            if not content_type.startswith(self.PDF_CONTENT_TYPE):
                raise ValueError(f"Fetched content is not a valid PDF. Content-Type: {content_type}")

            return response.content

        except requests.RequestException as e:
            raise ValueError(f"Error during API call to fetch PDF: {str(e)}")
