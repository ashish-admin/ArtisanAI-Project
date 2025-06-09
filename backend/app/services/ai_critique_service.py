# backend/app/services/ai_critique_service.py

import uuid
import vertexai
from vertexai.generative_models import GenerativeModel, Part

from app.schemas.critique import CritiqueRequest, AgentResponse, CritiqueSession, ConversationTurn

# In-memory session storage. For production, use a persistent store like Redis.
critique_sessions: dict[str, CritiqueSession] = {}

class AICritiqueService:
    """
    Service for handling the AI critique generation with an agentic workflow.
    """

    def _create_initial_analysis_prompt(self, request: CritiqueRequest) -> str:
        """Creates a prompt for the AI to analyze the user's request."""
        return (
            "You are an expert literary agent. Your goal is to provide the most helpful critique possible. "
            "First, analyze the user's writing and their request.\n\n"
            f"User's Goal: {request.goal}\n"
            f"Writing Length: {len(request.context)} characters\n\n"
            "Based on this, determine if you can provide a high-quality critique immediately, or if you need to ask a clarifying question. "
            "For example, if the text is very long and the request is broad (e.g., 'critique the dialogue'), it's better to ask for focus. "
            "If the request is clear and the text is short, you can proceed directly.\n\n"
            "Respond in one of two ways:\n"
            "1. If you need clarification, respond with: '[QUESTION] Your clarifying question here.'\n"
            "2. If you can proceed, respond with: '[PROCEED]'"
        )

    def _create_final_critique_prompt(self, session: CritiqueSession) -> str:
        """Constructs the final, detailed prompt for the LLM."""
        history = "\n".join(
            [f"Agent: {turn.agent_message}\nUser: {turn.user_response}" for turn in session.conversation_history]
        )

        prompt = (
            f"**Objective:** Critique the following text based on the user's goal: '{session.initial_request.goal}'.\n\n"
            f"**Persona:** Adopt the persona of a '{session.initial_request.persona}'.\n\n"
            f"**Output Format:** The critique should be structured as a '{session.initial_request.format}'.\n\n"
            f"**Constraints & Keywords:** The user has specified the following constraints and keywords to consider: {', '.join(session.initial_request.constraints)}.\n\n"
            f"**Conversation History (for additional context):**\n{history}\n\n"
            f"**Text for Critique:**\n---\n{session.initial_request.context}\n---\n\n"
            f"**Critique:**"
        )
        return prompt

    async def _generate_response(self, prompt: str) -> str:
        """Generates content from the Gemini model."""
        model = GenerativeModel("gemini-1.5-flash-001")
        try:
            response = await model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred while generating the critique: {e}"

    async def start_critique_session(self, request: CritiqueRequest) -> AgentResponse:
        """Starts a new critique session, either asking a question or giving the final critique."""
        session_id = str(uuid.uuid4())
        
        # Step 1: Initial Analysis by the AI
        analysis_prompt = self._create_initial_analysis_prompt(request)
        analysis_response = await self._generate_response(analysis_prompt)

        session = CritiqueSession(session_id=session_id, initial_request=request)
        critique_sessions[session_id] = session

        # Step 2: Decide whether to ask a question or proceed
        if analysis_response.strip().startswith("[QUESTION]"):
            question = analysis_response.replace("[QUESTION]", "").strip()
            session.conversation_history.append(ConversationTurn(agent_message=question))
            return AgentResponse(session_id=session_id, agent_message=question)
        else:
            final_prompt = self._create_final_critique_prompt(session)
            final_critique = await self._generate_response(final_prompt)
            session.final_critique = final_critique
            session.is_complete = True
            return AgentResponse(
                session_id=session_id,
                agent_message="Here is your critique:",
                is_final=True,
                final_critique=final_critique,
                engineered_prompt=final_prompt,
            )

    async def refine_critique(self, refinement_request: dict) -> AgentResponse:
        """Handles a user's response to a clarifying question."""
        session_id = refinement_request.get("session_id")
        user_response = refinement_request.get("user_response")

        if not session_id or session_id not in critique_sessions:
            raise ValueError("Invalid session ID.")
        
        session = critique_sessions[session_id]
        if session.is_complete:
            raise ValueError("This session is already complete.")

        # Update conversation history
        session.conversation_history[-1].user_response = user_response

        # Generate final critique
        final_prompt = self._create_final_critique_prompt(session)
        final_critique = await self._generate_response(final_prompt)
        session.final_critique = final_critique
        session.is_complete = True

        return AgentResponse(
            session_id=session_id,
            agent_message="Thank you for the clarification. Here is your refined critique:",
            is_final=True,
            final_critique=final_critique,
            engineered_prompt=final_prompt,
        )

ai_critique_service = AICritiqueService()