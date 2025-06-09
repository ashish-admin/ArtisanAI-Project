// Path: backend/app/api/v1/api.py

from fastapi import APIRouter
from app.api.v1.endpoints import auth, critique, projects, llm_suggestions

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(critique.router, prefix="/agent", tags=["AI Agent"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(llm_suggestions.router, prefix="/llm-suggestions", tags=["LLM Suggestions"])