# artisan_ai_backend/app/routers/llm_suggestions.py
from fastapi import APIRouter, Depends
from typing import List # Not strictly needed here if response model handles it, but good for clarity

# Use relative imports for modules within the 'app' package
from .. import models # For LLMRecommendationRequest and LLMRecommendationResponse
from .. import auth   # For get_current_active_user dependency
from .. import llm_recommender # The new logic file

router = APIRouter(
    prefix="/api/v1/llm-suggestions",
    tags=["LLM Suggestions"], # Tag for API docs
    dependencies=[Depends(auth.get_current_active_user)] # Secure this endpoint
)

@router.post("/", response_model=models.LLMRecommendationResponse)
async def suggest_llms_for_prompt(
    request_data: models.LLMRecommendationRequest # Expects data matching this Pydantic model
):
    """
    Provides LLM recommendations based on detailed prompt parameters.
    Analyzes the goal, format, context, and constraints to suggest suitable LLMs.
    """
    print(f">>> Endpoint: suggest_llms_for_prompt called with goal: {request_data.userGoal}")
    
    try:
        recommendations = llm_recommender.get_llm_recommendations(request_data)
        print(f">>> LLM Recommender returned {len(recommendations.suggestions)} suggestions.")
        return recommendations
    except Exception as e:
        # Log the error for server-side debugging
        print(f"Error in LLM suggestion endpoint: {e}")
        import traceback
        print(traceback.format_exc())
        # Re-raise as an HTTPException so FastAPI returns a proper error response
        # You might want a more specific error model for the client here too
        raise HTTPException(status_code=500, detail=f"An internal error occurred while generating LLM suggestions: {str(e)}")