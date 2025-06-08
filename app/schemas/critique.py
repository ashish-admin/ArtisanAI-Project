# app/schemas/critique.py
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# CORRECTED: The comment is now correctly formatted.
# This schema defines the data structure for the initial request
# to our AI Critique Agent.
class CritiqueRequest(BaseModel):
    """
    Pydantic schema for a user's request to the AI Critique Agent.
    This model gathers all necessary information from the frontend.
    """
    # The core text the user wants critiqued.
    writing_text: str

    # Parameters from the co-pilot flow that guide the critique.
    critique_goal: str  # e.g., "Critique plot pacing," "Check for passive voice"
    critique_persona: Optional[str] = None # e.g., "Professional book editor", "Casual reader"

    # We can include a generic 'options' dictionary for future flexibility,
    # allowing the frontend to send other parameters without backend changes.
    options: Optional[Dict[str, Any]] = None


# This schema defines the structured response from the AI Critique Agent.
class CritiqueResponse(BaseModel):
    """
    Pydantic schema for the structured response from the AI Critique Agent.
    This provides a much richer result than a single block of text.
    """
    # The main, high-level critique of the writing.
    main_critique: str

    # A list of specific, actionable suggestions for improvement.
    # This allows the frontend to display them as a checklist or bullet points.
    suggested_improvements: List[str]

    # An optional field for the agent to ask for clarification if the user's
    # request was ambiguous. This enables our interactive refinement loop.
    clarification_question: Optional[str] = None

    # A summary of the positive aspects of the writing.
    positive_feedback: Optional[str] = None