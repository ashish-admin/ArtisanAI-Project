# backend/app/core/config.py

from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List, Union

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    PROJECT_NAME: str = "Artisan AI"
    API_V1_STR: str = "/api/v1"

    # Security settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Database URL
    DATABASE_URL: str

    # CORS settings
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://your-frontend-domain.com", # Add your frontend domain
    ]

    # Google Cloud settings
    # This is the path to your service account key file
    GOOGLE_APPLICATION_CREDENTIALS: Union[str, None] = None
    GCP_PROJECT_ID: Union[str, None] = None
    GCP_LOCATION: Union[str, None] = None

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()