# app/api/v1/api.py
from fastapi import APIRouter

from app.api.v1.endpoints import auth, projects, critique

# CORRECTED: The comment is now correctly formatted.
# Create the main router for the v1 API.
# All routes included in this router will be prefixed with /api/v1,
# which is handled by the main app in main.py.
api_router = APIRouter()

# Include each of the feature-specific routers.
# This keeps our endpoint definitions organized and modular.
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(projects.router, prefix="/projects", tags=["Writing Projects"])
api_router.include_router(critique.router, prefix="/critique", tags=["AI Critique Agent"])