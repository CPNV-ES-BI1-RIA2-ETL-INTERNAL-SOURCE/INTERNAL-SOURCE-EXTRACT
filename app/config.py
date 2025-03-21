"""Application configuration."""
from functools import lru_cache
from pydantic import BaseModel
from typing import Optional

class Settings(BaseModel):
    """Application settings."""
    
    # API Configuration
    pdf_api_base_url: str = "http://localhost:8000"
    
    # OCR Configuration
    pdftotext_path: str = "pdftotext"
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings."""
    return Settings() 