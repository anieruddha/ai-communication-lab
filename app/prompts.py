def build_evaluation_prompt(text: str) -> str:
    """
    Builds a strict evaluation prompt for the LLM.
    The model MUST return only valid JSON matching the schema.
    """

    return f"""
        You are an expert communication evaluator.
        
        Evaluate the following text using the rubric below.
        Return STRICT JSON only.
        Do not include markdown.
        Do not include explanations.
        Do not include extra text.
        You MUST return JSON matching this exact schema:
        JSON schema:
        {{
          "mode": "professional" | "technical" | "clarity",
          "style": "neutral" | "strict_corporate" | "engineering_peer" | "communication_coach",
          "rubric_version": string,
          "dimensions": [
            {{
              "name": string,
              "score": number between 0 and 10,
              "reasoning": string
            }}
          ],
          "strengths": [string],
          "weaknesses": [string],
          "rewrite_suggestion": string,
          "rewrite_example": string
        }}
        
        Requirements:
        - mode MUST be "clarity"
        - style MUST be "communication_coach"
        - rubric_version MUST be "1.0"
        
        - Provide exactly 5 dimensions with these exact names:
          1. readability
          2. coherence
          3. ambiguity
          4. redundancy
          5. vocabulary
        - score must be a number between 0 and 10 (can be decimal)
        - strengths must contain at least 1 item
        - weaknesses must contain at least 1 item
        
        Text to evaluate:
        \"\"\"
        {text}
        \"\"\"
        """
