# backend/app/schemas/critique.py

from pydantic import BaseModel, Field
from typing import List, Optional

# Defines the structure for the initial critique request
class CritiqueRequest(BaseModel):
    goal: str
    format: str
    context: str # This will be the creative writing text
    constraints: List[str]
    persona: str
    project_id: Optional[int] = None

# Defines the structure for a follow-up refinement request
class CritiqueRefinementRequest(BaseModel):
    session_id: str
    user_response: str

# Represents a single conversational turn
class ConversationTurn(BaseModel):
    agent_message: str
    user_response: Optional[str] = None

# Full state of a critique session
class CritiqueSession(BaseModel):
    session_id: str
    initial_request: CritiqueRequest
    conversation_history: List[ConversationTurn] = []
    final_critique: Optional[str] = None
    is_complete: bool = False

# The response from the AI, which could be a question or the final critique
class AgentResponse(BaseModel):
    session_id: str
    agent_message: str
    is_final: bool = False
    final_critique: Optional[str] = None
    engineered_prompt: Optional[str] = None