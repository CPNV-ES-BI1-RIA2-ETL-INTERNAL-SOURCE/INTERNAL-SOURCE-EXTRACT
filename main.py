from fastapi import FastAPI
from app.api.router import router

# Create FastAPI app
app = FastAPI(
    title="PDF Text Extraction API",
    description="Extract text from PDF files using OCR",
    version="1.0.0"
)

# Add routes
app.include_router(router)