# Path: backend/app/core/config.py

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and defaults.
    """
    # From .env
    SECRET_KEY: str
    DATABASE_URL: str
    GOOGLE_API_KEY: str

    # Defaults
    PROJECT_NAME: str = "Synaptiq.ai"
    API_V1_STR: str = "/api/v1"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 # 1 hour

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()