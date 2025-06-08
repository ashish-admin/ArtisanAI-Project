app/api/v1/endpoints/critique.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any

from app.api import deps
from app.schemas import critique as critique_schema
from app.services import ai_critique_service
from app.db.base import User # Used for type hinting the current_user dependency

Create a new API router for the AI critique service
router = APIRouter()

@router.post("/", response_model=critique_schema.CritiqueResponse)
def get_writing_critique(
*,
critique_in: critique_schema.CritiqueRequest,
current_user: User = Depends(deps.get_current_active_user),
) -> Any:
"""
Get an AI-powered critique for a piece of creative writing.

This is a protected endpoint that requires authentication.
It takes the user's writing and critique parameters, sends them to the
AI agent service (powered by Gemini), and returns a structured critique.
"""
if not critique_in.writing_text or not critique_in.writing_text.strip():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Writing text cannot be empty.",
    )

# Call the core AI service to get the critique
critique = ai_critique_service.get_ai_critique(request=critique_in)

if not critique or not critique.main_critique:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to get a valid critique from the AI agent.",
    )

return critique
