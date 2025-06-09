# backend/app/main.py

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import vertexai

from app.api.v1.api import api_router
from app.core.config import settings

# Initialize Vertex AI
# This needs to be done before any other calls to the Vertex AI SDK
vertexai.init(project=settings.GCP_PROJECT_ID, location=settings.GCP_LOCATION)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    """
    An endpoint to confirm the API is running.
    """
    return {"message": "Welcome to Artisan AI's Backend"}