// Path: backend/app/routers/llm_suggestions.py

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Dict

from app.api import deps
from app.schemas.user import User

router = APIRouter()

class SuggestionRequest(BaseModel):
    goal: str

class LlmSuggestion(BaseModel):
    model_name: str
    strengths: str
    reason: str

LLM_KNOWLEDGE_BASE = {
    "gemini-1.5-pro": {
        "strengths": "Multimodal, long context, complex reasoning",
        "keywords": ["video", "audio", "image", "multimodal", "large document", "complex"],
    },
    "gemini-1.5-flash": {
        "strengths": "Fast, high-quality, cost-effective",
        "keywords": ["fast", "quick", "summary", "general", "classification"],
    },
    "claude-3-opus": {
        "strengths": "Top-tier performance, deep reasoning, analysis",
        "keywords": ["analysis", "research", "detailed", "writing", "creative"],
    },
    "gpt-4o": {
        "strengths": "Excellent conversational ability, strong general knowledge",
        "keywords": ["conversation", "chatbot", "dialogue", "general purpose"],
    },
    "llama-3-70b": {
        "strengths": "Top open-weight model, good for instruction following",
        "keywords": ["open source", "custom", "fine-tune"],
    },
    "mistral-large": {
        "strengths": "Strong reasoning, multilingual, cost-effective for large scale",
        "keywords": ["multilingual", "french", "german", "spanish", "italian", "code"],
    },
}

@router.post("/", response_model=List[LlmSuggestion])
async def get_llm_suggestions(
    request: SuggestionRequest,
    current_user: User = Depends(deps.get_current_user),
):
    """
    Provides tailored LLM suggestions based on the user's goal.
    """
    goal_text = request.goal.lower()
    suggestions = []
    
    for model, data in LLM_KNOWLEDGE_BASE.items():
        if any(keyword in goal_text for keyword in data["keywords"]):
            suggestions.append(
                LlmSuggestion(
                    model_name=model,
                    strengths=data["strengths"],
                    reason=f"Recommended for tasks involving keywords like: {', '.join(data['keywords'])}."
                )
            )

    if not suggestions:
        default_models = ["gemini-1.5-flash", "gpt-4o", "claude-3-opus"]
        for model in default_models:
            data = LLM_KNOWLEDGE_BASE[model]
            suggestions.append(
                 LlmSuggestion(
                    model_name=model,
                    strengths=data["strengths"],
                    reason="A great general-purpose model suitable for a wide range of tasks."
                )
            )
            
    return suggestions[:3]