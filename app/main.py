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

if __name__ == "__main__":
    init_db()