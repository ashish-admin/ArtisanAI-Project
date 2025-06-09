# backend/app/schemas/critique.py

from pydantic import BaseModel
from typing import List, Optional

# Defines the structure for a critique request from the frontend
class CritiqueRequest(BaseModel):
    goal: str
    format: str
    context: str # This will be the creative writing text
    constraints: List[str]
    persona: str
    project_id: Optional[int] = None # Optional: link to a saved project

# Defines the structure for the AI's response
class CritiqueResponse(BaseModel):
    engineered_prompt: str
    critique_text: str
    llm_suggestion: str