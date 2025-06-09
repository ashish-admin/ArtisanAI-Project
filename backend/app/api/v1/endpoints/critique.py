# backend/app/api/v1/endpoints/critique.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.schemas.critique import CritiqueRequest, CritiqueResponse
from app.services.ai_critique_service import ai_critique_service
from app.schemas.user import User

router = APIRouter()

@router.post("/refine-prompt", response_model=CritiqueResponse, status_code=status.HTTP_200_OK)
async def refine_prompt(
    critique_request: CritiqueRequest,
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db),
):
    """
    Receives writing and critique parameters, and returns an AI-generated critique.
    - Requires authentication.
    """
    response = await ai_critique_service.get_critique(critique_request)
    return response