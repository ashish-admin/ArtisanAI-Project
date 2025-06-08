# app/services/ai_critique_service.py
import json
from typing import Dict, Any

# We will use the Vertex AI library for enterprise-grade access to Gemini
import vertexai
from vertexai.generative_models import GenerativeModel, Part

from app.core.config import GCP_PROJECT_ID, GCP_LOCATION
from app.schemas.critique import CritiqueRequest, CritiqueResponse

# --- Vertex AI Initialization ---
# This block initializes the Vertex AI client once when the module is loaded.
# It uses the project ID and location from our central config file.
try:
    print(">>> Initializing Vertex AI for Critique Service...")
    vertexai.init(project=GCP_PROJECT_ID, location=GCP_LOCATION)
    print(">>> Vertex AI initialized successfully.")
except Exception as e:
    print(f"!!! FATAL ERROR: Could not initialize Vertex AI. "
          f"Ensure the API is enabled and your project/location are correct. Error: {e}")


# --- The "Meta-Prompt" for our AI Agent (System Instruction) ---
# This is a critical piece of engineering that defines the "persona" and
# capabilities of our own AI agent.
AGENT_SYSTEM_INSTRUCTION = """
You are an expert-level "Literary Editor AI." Your purpose is to provide insightful, constructive, and actionable critiques on creative writing.

When you receive a user's text and their critique goal, you must:
1.  **Analyze and Understand:** Deeply analyze the user's text and their specific critique goal (e.g., "critique plot pacing," "check for passive voice," "improve dialogue realism").
2.  **Provide High-Level Feedback:** Start with a concise, high-level summary of the writing's main strengths and areas for improvement related to the user's goal.
3.  **Generate Actionable Suggestions:** Create a specific, numbered list of suggested improvements. Each suggestion should be clear and practical. For example, instead of "the dialogue is weak," suggest "The dialogue in paragraph 3 feels unnatural. Try reading it aloud. Consider rephrasing John's line to be more direct to show his frustration."
4.  **Offer Positive Reinforcement:** Identify something that the user did well and mention it in a dedicated positive feedback section. This is crucial for encouragement.
5.  **Ask for Clarification (If Needed):** If the user's request is ambiguous (e.g., asking for a "general critique" on a very long text), your primary response should be a single, targeted question to help them narrow their focus. In this case, the other fields can be brief.

You MUST return your response as a single, valid JSON object with the following keys: "main_critique", "suggested_improvements", "positive_feedback", "clarification_question". Do not include any other text or markdown formatting outside of this JSON object.
"""

def _create_agent_prompt_for_user(request: CritiqueRequest) -> str:
    """Helper function to format the user's request into a clear prompt for the agent."""
    
    # Constructing a detailed prompt for our agent to work with.
    user_prompt_summary = f"""
    A user has submitted a piece of creative writing for critique. Please analyze it based on the following parameters:

    **User's Primary Critique Goal:**
    {request.critique_goal}

    **AI Persona for Critique:**
    Please adopt the persona of a: {request.critique_persona or "Helpful and constructive writing coach."}

    **User's Writing Text to be Critiqued:**
    --- START OF TEXT ---
    {request.writing_text}
    --- END OF TEXT ---

    Please provide your analysis in the required JSON format.
    """
    return user_prompt_summary

def get_ai_critique(request: CritiqueRequest) -> CritiqueResponse:
    """
    Uses the Vertex AI Gemini Pro API to generate a critique for a user's writing.
    """
    try:
        # Initialize the Vertex AI Gemini Pro model with our system instruction.
        # 'gemini-1.5-pro-preview-0409' is an example of a specific version.
        # You can use 'gemini-1.5-pro' for the latest stable release.
        model = GenerativeModel(
            "gemini-1.5-pro-preview-0409",
            system_instruction=Part.from_text(AGENT_SYSTEM_INSTRUCTION)
        )
        
        user_prompt_for_agent = _create_agent_prompt_for_user(request)
        
        # Generate the content using the Vertex AI client
        response = model.generate_content(user_prompt_for_agent)
        
        # The Vertex AI response object structure is slightly different. We extract the text.
        cleaned_response_text = response.text.strip().replace("```json", "").replace("```", "").strip()
        response_data = json.loads(cleaned_response_text)

        # Create our Pydantic response model from the parsed JSON data
        critique_response = CritiqueResponse(
            main_critique=response_data.get("main_critique", "No high-level critique was generated."),
            suggested_improvements=response_data.get("suggested_improvements", []),
            positive_feedback=response_data.get("positive_feedback"),
            clarification_question=response_data.get("clarification_question")
        )
        return critique_response

    except Exception as e:
        print(f"!!! ERROR during Vertex AI call in ai_critique_service: {e}")
        # In case of any error, return a structured error response
        return CritiqueResponse(
            main_critique=f"An error occurred while generating the critique. Please check the backend server logs. Error: {str(e)}",
            suggested_improvements=[],
            positive_feedback="Could not analyze for positive feedback due to an error."
        )
