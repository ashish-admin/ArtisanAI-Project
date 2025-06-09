# backend/app/api/v1/endpoints/critique.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.schemas.critique import CritiqueRequest, AgentResponse
from app.services.ai_critique_service import ai_critique_service
from app.schemas.user import User

router = APIRouter()

@router.post("/start-critique", response_model=AgentResponse, status_code=status.HTTP_200_OK)
async def start_critique(
    critique_request: CritiqueRequest,
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db),
):
    """
    Starts a new critique session.
    The AI will either provide a critique directly or ask a clarifying question.
    """
    try:
        response = await ai_critique_service.start_critique_session(critique_request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/refine-critique", response_model=AgentResponse, status_code=status.HTTP_200_OK)
async def refine_critique(
    refinement_request: dict,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Continues a critique session by providing a response to the AI's question.
    """
    try:
        response = await ai_critique_service.refine_critique(refinement_request)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))