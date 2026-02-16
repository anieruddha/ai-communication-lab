import re

import httpx
from pydantic import ValidationError

from app.models import EvaluationResult
from app.observability import observe_execution
from app.prompts import build_evaluation_prompt

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:7b-instruct"


def _clean_model_output(text: str) -> str:
    # Remove triple backtick blocks
    fenced = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if fenced:
        return fenced.group(1).strip()

    return text.strip()


@observe_execution()
def evaluate_with_llm(text: str) -> EvaluationResult:
    """
    Sends text to Ollama for evaluation.
    Validates response using Pydantic.
    Returns structured EvaluationResult.
    """

    prompt = build_evaluation_prompt(text)
    response = httpx.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0
            }
        },
        timeout=120
    )

    response.raise_for_status()
    data = response.json()
    raw_output = data["response"]
    cleaned = _clean_model_output(raw_output)
    validated = EvaluationResult.model_validate_json(cleaned)
    return validated

    try:
        return EvaluationResult.model_validate_json(raw_output)
    except ValidationError as e:
        raise ValueError(f"Invalid JSON returned by model:\n{raw_output}") from e
