# app/main.py
from fastapi import FastAPI
from app.core.config import API_V1_STR
from app.api.v1.api import api_router
from app.db.session import engine
from app.db import base as base_models

# This command instructs SQLAlchemy to create all tables defined in app/db/base.py
base_models.Base.metadata.create_all(bind=engine)

# Create the main FastAPI application instance.
app = FastAPI(
    title="Artisan AI - Critique Agent API",
    description="API for managing users, writing projects, and getting AI-powered critiques.",
    version="1.0.0",
    openapi_url=f"{API_V1_STR}/openapi.json"
)

# Include the main API router from api/v1/api.py
# The prefix="/api/v1" ensures all included routes start with that path.
app.include_router(api_router, prefix=API_V1_STR)

@app.get("/", tags=["Health Check"])
def read_root():
    """
    Root endpoint for basic health check.
    """
    return {"status": "ok", "message": "Welcome to the Artisan AI Backend!"}