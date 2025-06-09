# backend/app/api/v1/api.py

from fastapi import APIRouter
from app.api.v1.endpoints import auth, critique, projects

api_router = APIRouter()

# Include authentication routes (e.g., /register, /token)
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Include AI agent routes (e.g., /agent/refine-prompt)
api_router.include_router(critique.router, prefix="/agent", tags=["AI Agent"])

# Include project management routes (e.g., /projects/)
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])