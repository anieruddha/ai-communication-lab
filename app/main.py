from app.llm_engine import evaluate_with_llm
from app.storage import init_db, save_evaluation

def run_llm_pipeline(text: str):
    result = evaluate_with_llm(text)
    save_evaluation(text, result)
    return result


if __name__ == "__main__":
    init_db()
