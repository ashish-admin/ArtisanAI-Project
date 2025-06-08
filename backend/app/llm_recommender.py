# artisan_ai_backend/app/llm_recommender.py
from typing import List, Dict, Any
# Ensure models are imported correctly based on your project structure
# If llm_recommender.py is in the same 'app' directory as models.py:
from .models import LLMRecommendationRequest, LLMSuggestion, LLMRecommendationResponse 

# --- Mock/Placeholder LLM Knowledge Base ---
# This would ideally be in a database, configuration file, or regularly updated.
LLM_KNOWLEDGE_BASE = [
    {
        "id": "gemini_advanced", "name": "Gemini Advanced / 1.5 Pro",
        "strengths": ["complex_reasoning", "coding_expert", "multimodal_strong", "long_context_large", "analysis_deep"],
        "keywords": ["gemini", "advanced", "pro 1.5"],
        "type": "premium", "cost_tier": 3, "speed_rating": 2, # 1=fastest/cheapest, 3=slowest/priciest
        "notes": "Google's most capable model for highly complex tasks."
    },
    {
        "id": "gemini_pro_standard", "name": "Gemini Pro (Standard)",
        "strengths": ["general_reasoning", "creative_writing_good", "summarization_good", "coding_good", "multimodal_basic"],
        "keywords": ["gemini", "pro"],
        "type": "standard", "cost_tier": 2, "speed_rating": 2,
        "notes": "Solid all-around model, good for general content and coding."
    },
    {
        "id": "gemini_flash", "name": "Gemini Flash",
        "strengths": ["speed_fast", "cost_effective", "summarization_quick", "simple_q&a", "chat"],
        "keywords": ["gemini", "flash"],
        "type": "lite", "cost_tier": 1, "speed_rating": 1,
        "notes": "Optimized for speed and efficiency, great for high-volume tasks."
    },
    {
        "id": "gpt_4_series", "name": "GPT-4 Series (e.g., Turbo, Omni)",
        "strengths": ["complex_reasoning", "coding_expert", "creative_writing_excellent", "knowledge_extensive", "analysis_deep"],
        "keywords": ["gpt-4", "gpt4", "openai"],
        "type": "premium", "cost_tier": 3, "speed_rating": 2,
        "notes": "OpenAI's flagship models, known for strong reasoning and generation."
    },
    {
        "id": "gpt_3_5_series", "name": "GPT-3.5 Series (e.g., Turbo)",
        "strengths": ["speed_fast", "cost_effective", "general_q&a", "prototyping", "chat"],
        "keywords": ["gpt-3.5", "gpt3.5", "openai"],
        "type": "standard", "cost_tier": 1, "speed_rating": 1,
        "notes": "Fast and affordable for general tasks and chatbots."
    },
    {
        "id": "claude_3_opus", "name": "Claude 3 Opus",
        "strengths": ["long_context_excellent", "complex_reasoning", "creative_writing_excellent", "analysis_deep", "reliability_high"],
        "keywords": ["claude", "opus", "anthropic"],
        "type": "premium", "cost_tier": 3, "speed_rating": 2,
        "notes": "Anthropic's most powerful model, excels at long context and nuanced tasks."
    },
    {
        "id": "claude_3_sonnet", "name": "Claude 3 Sonnet",
        "strengths": ["balanced_performance", "long_context_good", "summarization_good", "coding_good", "enterprise_ready"],
        "keywords": ["claude", "sonnet", "anthropic"],
        "type": "standard", "cost_tier": 2, "speed_rating": 2,
        "notes": "Good balance of intelligence and speed for enterprise workloads."
    },
    {
        "id": "claude_3_haiku", "name": "Claude 3 Haiku",
        "strengths": ["speed_very_fast", "cost_effective", "responsiveness_high", "simple_q&a"],
        "keywords": ["claude", "haiku", "anthropic"],
        "type": "lite", "cost_tier": 1, "speed_rating": 1,
        "notes": "Fastest and most compact model in the Claude 3 family for near-instant responsiveness."
    },
    {
        "id": "code_llama_series", "name": "Code Llama Series (e.g., 70B)",
        "strengths": ["coding_expert", "code_completion", "code_explanation", "debugging"],
        "keywords": ["code llama", "llama", "meta"],
        "type": "specialized_coding", "cost_tier": 2, "speed_rating": 2, # Varies by size
        "notes": "Meta's open models specialized for code generation and understanding."
    },
    # Add more LLMs as needed
]

def _calculate_score(llm_data: Dict[str, Any], request: LLMRecommendationRequest) -> float:
    score = 0.0
    reason_segments = []

    goal_lower = request.userGoal.lower()
    format_lower = request.selectedOutputFormat.lower()
    context_lower = (request.contextProvided or "").lower()
    tone_lower = (request.constraints.tone or "").lower()
    prioritize_quality = request.constraints.prioritizeQuality if request.constraints.prioritizeQuality is not None else True
    
    llm_strengths = llm_data.get("strengths", [])
    llm_type = llm_data.get("type", "standard")

    # Priority Scoring
    if prioritize_quality:
        if llm_type == "premium": score += 3.0; reason_segments.append("suited for high quality demands")
        elif llm_type == "standard": score += 1.0
    else: # Prioritize speed/cost
        if llm_type == "lite": score += 3.0; reason_segments.append("cost-effective and fast")
        elif llm_type == "standard": score += 1.0
        if llm_data.get("speed_rating") == 1: score += 1.0 # Bonus for fastest if speed is priority
    
    # Coding tasks
    if any(kw in goal_lower for kw in ["code", "script", "develop", "program"]) or \
       any(kw in format_lower for kw in ["code", "json", "script"]) or \
       any(kw in context_lower for kw in ["python", "javascript", "java", "c#", "typescript", "dart"]):
        if "coding_expert" in llm_strengths: score += 5.0; reason_segments.append("expert coding capabilities")
        elif "coding_good" in llm_strengths: score += 3.0; reason_segments.append("good for coding tasks")
        if llm_type == "specialized_coding": score += 2.0; reason_segments.append("specialized for code")

    # Creative writing
    if any(kw in goal_lower for kw in ["story", "poem", "narrative", "creative writing"]) or \
       tone_lower == "creative":
        if "creative_writing_excellent" in llm_strengths: score += 5.0; reason_segments.append("excellent for creative writing")
        elif "creative_writing_good" in llm_strengths: score += 3.0; reason_segments.append("good for creative writing")

    # Summarization
    if "summarize" in goal_lower or "summary" in format_lower:
        if "summarization_good" in llm_strengths: score += 4.0; reason_segments.append("strong summarization")
        elif "summarization_quick" in llm_strengths: score += 3.0; reason_segments.append("quick summarization")

    # Analysis / Complex Reasoning / Long Context
    if any(kw in goal_lower for kw in ["analyze", "analysis", "research", "report", "explain complex"]) or \
       "detailed explanation" in format_lower or \
       len(request.contextProvided or "") > 1000: # Example: long context indicated by input length
        if "complex_reasoning" in llm_strengths: score += 3.0; reason_segments.append("handles complex reasoning")
        if "analysis_deep" in llm_strengths: score += 2.0; reason_segments.append("suited for deep analysis")
        if "long_context_excellent" in llm_strengths: score += 3.0; reason_segments.append("excels with long contexts")
        elif "long_context_large" in llm_strengths: score += 2.0; reason_segments.append("supports large contexts")
        elif "long_context_good" in llm_strengths: score += 1.0; reason_segments.append("good with long contexts")

    # General Q&A / Chat
    if any(kw in goal_lower for kw in ["q&a", "question", "answer", "chat", "conversation"]) or \
       "dialogue" in format_lower:
        if "simple_q&a" in llm_strengths: score += 2.0; reason_segments.append("good for Q&A")
        if "chat" in llm_strengths: score += 2.0; reason_segments.append("effective for chat")
        
    # TODO: Add more rules based on persona, specific keywords in context, length constraints etc.
    
    # Deduct points if known weaknesses or anti-patterns for the request (not implemented yet)

    # Add a small base score if no other rules hit significantly
    if score < 1.0 and llm_type != "specialized_coding" and not (any(kw in goal_lower for kw in ["code", "script"])):
        score += 0.5 # Small boost for general purpose models if no strong match

    return score, reason_segments


def get_llm_recommendations(request: LLMRecommendationRequest) -> LLMRecommendationResponse:
    scored_llms: List[Dict[str, Any]] = []

    for llm_data in LLM_KNOWLEDGE_BASE:
        score, reason_segments = _calculate_score(llm_data, request)
        if score > 0: # Only consider models that scored positively
            scored_llms.append({
                "data": llm_data,
                "score": score,
                "reason_segments": list(set(reason_segments)) # Unique reasons
            })

    # Sort LLMs by score in descending order
    sorted_llms = sorted(scored_llms, key=lambda item: item["score"], reverse=True)
    
    suggestions: List[LLMSuggestion] = []
    notes = ""
    
    top_n = 3 # Number of top suggestions to return
    for item in sorted_llms[:top_n]:
        llm = item["data"]
        score = item["score"]
        reason = f"{llm['name']}: "
        if item["reason_segments"]:
            reason += ", ".join(item["reason_segments"][:3]) + "." # Show top 3 reasons
        else:
            reason += llm.get("notes", "A generally capable model.")
        
        # Normalize score to a 0-1 confidence (this is a very rough example)
        # Max possible score could be estimated or use a dynamic normalization.
        # Let's assume a conceptual max score around 15 for this example.
        confidence = min(1.0, score / 15.0) if score > 0 else 0.0

        suggestions.append(LLMSuggestion(
            llm_name=llm["name"],
            reason=reason,
            confidence=confidence if confidence > 0.1 else None # Only show confidence if reasonably high
        ))

    if not suggestions:
        # Fallback if no scored LLMs met criteria
        suggestions.append(LLMSuggestion(
            llm_name="Gemini Pro (General Purpose)", 
            reason="A versatile model suitable for a wide range of tasks. Your request was too general for a specific recommendation.",
            confidence=0.4
        ))
        notes = "Could not determine a highly specific recommendation based on input; providing general purpose options."
        
    return LLMRecommendationResponse(suggestions=suggestions, notes=notes)