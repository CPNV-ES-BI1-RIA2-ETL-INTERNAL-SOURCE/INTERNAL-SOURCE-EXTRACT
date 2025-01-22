from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from datetime import date

from .JSONFormatter import JSONFormatter
from .OCRProcessor import OCRProcessor
from .pdfFetcher import PDFFetcher

api_router = APIRouter()

pdf_fetcher = PDFFetcher()
ocr_processor = OCRProcessor()
json_formatter = JSONFormatter()


@api_router.get("/process-pdf", response_model=list)
async def process_pdf(url: str):
    try:
        pdf_data = pdf_fetcher.fetch_pdf(url)

        extracted_text = ocr_processor.extract_text(pdf_data)

        formatted_json = json_formatter.format(extracted_text)

        return formatted_json

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="An internal server error occurred.")
