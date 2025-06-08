# app/main.py
from fastapi import FastAPI
from app.core.config import API_V1_STR
from app.api.v1.api import api_router
from app.db.session import engine
from app.db import base as base_models

# This command instructs SQLAlchemy to create all the tables defined in app/db/base.py
# (i.e., the User and Project tables) in the database if they don't already exist.
# This is a crucial step for the application to function on its first run.
base_models.Base.metadata.create_all(bind=engine)

# Create the main FastAPI application instance.
# We can define metadata like the title and version here, which will be
# visible in the auto-generated API documentation.
app = FastAPI(
    title="Artisan AI - Critique Agent API",
    openapi_url=f"{API_V1_STR}/openapi.json"
)

# Include the main API router.
# All routes defined in api_router (from auth.py, projects.py, critique.py)
# will be included under the /api/v1 prefix.
app.include_router(api_router, prefix=API_V1_STR)

# Optional: Add a root endpoint for simple health checks.
@app.get("/", status_code=200, tags=["Health Check"])
def read_root():
    """
    Root endpoint for basic health check.
    """
    return {"status": "ok", "message": "Welcome to the Artisan AI Backend!"}