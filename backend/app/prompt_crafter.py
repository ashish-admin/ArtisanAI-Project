# artisan_ai_backend/app/prompt_crafter.py
from typing import List, Optional, Dict, Any
# Ensure models are imported correctly. If prompt_crafter.py is in the 'app' directory
# alongside models.py, then "from .models import ..." is correct.
from .models import PromptCraftRequest, PromptCraftResponse, ConstraintsModel

# Helper class for string building
class StringBuffer:
    def __init__(self):
        self._buffer: List[str] = []

    def writeln(self, text: str = ""):
        self._buffer.append(text + "\n")

    def write(self, text: str = ""): 
        self._buffer.append(text)

    def toString(self) -> str:
        return "".join(self._buffer)

def _format_constraints_for_prompt(constraints: ConstraintsModel) -> tuple[str, List[str]]:
    parts: List[str] = []
    details: List[str] = ["Formatting user-defined constraints."] 

    # Ensure constraints fields are accessed safely, providing defaults if None
    length_constraint = constraints.length.strip() if constraints.length and constraints.length.strip() else ""
    tone_constraint = constraints.tone.strip() if constraints.tone and constraints.tone.strip() else ""
    include_keywords_constraint = constraints.includeKeywords.strip() if constraints.includeKeywords and constraints.includeKeywords.strip() else ""
    exclude_keywords_constraint = constraints.excludeKeywords.strip() if constraints.excludeKeywords and constraints.excludeKeywords.strip() else ""
    prioritize_quality_constraint = constraints.prioritizeQuality if constraints.prioritizeQuality is not None else True


    if length_constraint:
        parts.append(f"- **Desired Length:** Adhere to this length if possible: \"{length_constraint}\".")
        details.append(f"Constraint - Desired length: {length_constraint}")
    
    if tone_constraint:
        parts.append(f"- **Tone of Voice:** The response MUST adopt a \"{tone_constraint}\" tone.")
        details.append(f"Constraint - Tone: {tone_constraint}")

    if include_keywords_constraint:
        parts.append(f"- **Keywords/Phrases to Emphasize or Include:** Naturally integrate these: \"{include_keywords_constraint}\".")
        details.append(f"Constraint - Keywords to include: {include_keywords_constraint}")
        
    if exclude_keywords_constraint:
        parts.append(f"- **Keywords/Topics to Strictly Avoid:** Do NOT mention or allude to: \"{exclude_keywords_constraint}\".")
        details.append(f"Constraint - Keywords to exclude: {exclude_keywords_constraint}")
    
    priority_desc = "Your primary focus is on delivering the **highest quality, depth, and accuracy of reasoning**, even if it requires more elaborate processing or length." \
                    if prioritize_quality_constraint else \
                    "Your primary focus is on **speed and cost-effectiveness**; aim for conciseness and efficiency while still fully addressing the core goal."
    parts.append(f"- **Overall Output Priority:** {priority_desc}")
    details.append(f"Constraint - Overall priority set to: {'Quality/Reasoning' if prioritize_quality_constraint else 'Speed/Cost'}")
    
    has_textual_constraints = any(
        p.startswith("- **Desired Length") or \
        p.startswith("- **Tone of Voice") or \
        p.startswith("- **Keywords/Phrases to Emphasize") or \
        p.startswith("- **Keywords/Topics to Strictly Avoid") for p in parts
    )
    
    if not has_textual_constraints and len(parts) == 1: 
         return f"- {priority_desc} (No other specific textual constraints were provided beyond this general guidance.)\n", details
    
    return "\n".join(parts) + "\n", details


def craft_advanced_prompt(request: PromptCraftRequest) -> PromptCraftResponse:
    refinement_details: List[str] = ["Initiated advanced prompt construction process."]
    sb = StringBuffer()

    # --- Section 1: Overall Role & Task Clarification ---
    sb.writeln("### META-INSTRUCTION: ROLE & OBJECTIVE FOR AI ASSISTANT")
    sb.writeln("You are a highly proficient AI language model. Your primary objective is to meticulously analyze the following user request and generate a response that is accurate, relevant, coherent, and precisely adheres to all specified parameters.")
    refinement_details.append("Set general AI role and objective.")

    # --- Section 2: Core User Goal ---
    sb.writeln("\n### 1. PRIMARY GOAL / USER INTENT:")
    user_goal_stripped = request.userGoal.strip()
    sb.writeln(f"The user wants you to: **{user_goal_stripped}**")
    refinement_details.append(f"Extracted primary goal: {user_goal_stripped}")

    # --- Section 3: Persona (if provided and not skipped) ---
    persona_description_stripped = request.personaDescription.strip() if request.personaDescription else ""
    if not request.personaSkipped and \
       persona_description_stripped and \
       persona_description_stripped.lower() not in ["not specified (skipped)", "not specified"]:
        sb.writeln("\n### 2. PERSONA DIRECTIVE (Adopt this voice, style, and perspective):")
        sb.writeln(f"> You MUST respond as: **{persona_description_stripped}**.")
        sb.writeln("> All aspects of your language, tone, and the nature of your knowledge should fully embody this persona.")
        refinement_details.append(f"Instructed AI to adopt specific persona: {persona_description_stripped}")
    else:
        sb.writeln("\n### 2. PERSONA DIRECTIVE:")
        sb.writeln("> Adopt a neutral, objective, and highly helpful assistant persona. If the context of the goal implies a specific expertise (e.g., 'explain physics'), assume that expert role naturally.")
        refinement_details.append("Applied default (neutral or context-implied expert) assistant persona.")

    # --- Section 4: Essential Context & Background ---
    context_provided_stripped = request.contextProvided.strip() if request.contextProvided else ""
    if context_provided_stripped:
        sb.writeln("\n### 3. CRITICAL CONTEXT & BACKGROUND INFORMATION (Base your response on this):")
        sb.writeln("```text")
        sb.writeln(context_provided_stripped)
        sb.writeln("```")
        refinement_details.append("Included and formatted provided context block.")
    else:
        sb.writeln("\n### 3. CONTEXT & BACKGROUND INFORMATION:")
        sb.writeln("> No specific external context was provided. Rely on your general knowledge and the other instructions in this prompt.")
        refinement_details.append("Noted that no specific external context was provided.")

    # --- Section 5: Output Format Specifications ---
    selected_output_format_stripped = request.selectedOutputFormat.strip()
    sb.writeln("\n### 4. MANDATORY OUTPUT STRUCTURE & FORMAT:")
    sb.writeln(f"> The final output MUST be structured strictly as: **{selected_output_format_stripped}**.")
    format_lower = selected_output_format_stripped.lower()

    if "json" in format_lower:
        sb.writeln("> **JSON Specifics:** If the format is JSON, the output must be ONLY a single, valid JSON object or array. Do NOT include any introductory/explanatory text, markdown formatting (like ```json), or any characters outside the JSON structure itself. Validate your JSON structure before outputting.")
        refinement_details.append("Added strict instructions for JSON output formatting.")
    elif "code" in format_lower or "script" in format_lower:
        lang_guess = format_lower.replace("code snippet", "").replace("code", "").replace("script", "").strip()
        sb.writeln(f"> **Code Specifics:** If the format involves code (e.g., '{selected_output_format_stripped}'), provide ONLY the raw code block for the inferred language ({lang_guess if lang_guess else 'as appropriate'}). Do not include any surrounding explanatory text or markdown code fences unless the goal explicitly requests comments within the code.")
        refinement_details.append("Added strict instructions for code block output formatting.")
    elif "list" in format_lower:
        sb.writeln("> **List Specifics:** Ensure each item is clearly delineated (e.g., using markdown bullets '-' or numbers '1.' as appropriate for the specified list type).")
        refinement_details.append("Added guidance for list formatting.")
    elif "email" in format_lower:
        sb.writeln("> **Email Specifics:** Structure the response as a complete email, including appropriate salutations and closings if not otherwise specified in the goal or context. Pay attention to professional tone unless an alternative persona is active.")
        refinement_details.append("Added guidance for email structure.")
    refinement_details.append(f"Mandated output format: {selected_output_format_stripped}")
    
    # --- Section 6: Detailed Constraints and Guidelines ---
    constraints_str, constraint_details_list = _format_constraints_for_prompt(request.constraints)
    sb.writeln("\n### 5. DETAILED CONSTRAINTS & GUIDELINES (Strict Adherence Required):")
    sb.writeln(constraints_str) 
    refinement_details.extend(constraint_details_list)

    # --- Section 7: Advanced Prompting Techniques (Examples) ---
    goal_lower_for_techniques = user_goal_stripped.lower()
    prioritize_quality_for_techniques = request.constraints.prioritizeQuality if request.constraints.prioritizeQuality is not None else False
    
    if any(kw in goal_lower_for_techniques for kw in ["explain", "analyze", "plan", "develop a strategy", "reason about", "critique"]) or \
       (prioritize_quality_for_techniques):
        sb.writeln("### 6. SUGGESTED AI APPROACH & REASONING (Internal thought process encouragement):")
        sb.writeln("> For complex requests like this, briefly outline your plan or step-by-step thinking process internally before generating the final output. This ensures all facets of the request are addressed comprehensively and accurately. If helpful, use a scratchpad approach for complex calculations or multi-step reasoning, then synthesize the final answer clearly.")
        refinement_details.append("Encouraged internal step-by-step thinking/planning for complex tasks.")

    # --- Section 8: Final Instruction & Quality Check ---
    sb.writeln("\n### 7. FINAL INSTRUCTION & OUTPUT GENERATION:")
    sb.writeln("Review all the above sections (1-6) meticulously. Your response should be a direct and complete fulfillment of the PRIMARY OBJECTIVE, perfectly embodying the PERSONA DIRECTIVE (if specified), utilizing all CRITICAL CONTEXT, adhering strictly to the MANDATORY OUTPUT STRUCTURE, and respecting all DETAILED CONSTRAINTS & GUIDELINES. Prioritize accuracy, relevance, coherence, and thoroughness based on the Overall Output Priority.")
    sb.writeln("Proceed with generating the response now.")
    refinement_details.append("Added final comprehensive instruction and quality check reminder.")

    crafted_prompt_str = sb.toString()
    return PromptCraftResponse(crafted_prompt=crafted_prompt_str, refinement_details=refinement_details)