import json

from app.storage import init_db, save_evaluation
from app.models import EvaluationResult, DimensionScore
from app.llm_engine import evaluate_with_llm
from app.observability import observe_execution

observe_execution()
def run_llm_pipeline(text: str):
    result = evaluate_with_llm(text)
    save_evaluation(text, result)
    return result

def simulate():
    evaluation = EvaluationResult(
        mode="professional",
        style="neutral",
        rubric_version="v1.0",
        dimensions=[
            DimensionScore(name="tone", score=8, reasoning="Good tone"),
            DimensionScore(name="structure", score=7, reasoning="Decent flow"),
            DimensionScore(name="conciseness", score=6, reasoning="Some repetition"),
            DimensionScore(name="actionability", score=8, reasoning="Clear ask"),
            DimensionScore(name="confidence", score=7, reasoning="Mostly confident"),
        ],
        strengths=["Clear intent"],
        weaknesses=["Slightly verbose"],
        rewrite_suggestion="Tighten second paragraph.",
    )

    record_id = save_evaluation(
        input_text="Sample professional message.",
        evaluation=evaluation,
    )

    print(f"Saved evaluation with ID: {record_id}")


if __name__ == "__main__":
    init_db()