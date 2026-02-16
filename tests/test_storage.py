import tempfile
import os
from sqlalchemy import create_engine
from app.storage import Base, EvaluationORM
from app.models import EvaluationResult, DimensionScore
from app.storage import save_evaluation


def create_test_engine():
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()
    engine = create_engine(f"sqlite:///{temp_file.name}")
    return engine, temp_file.name


def test_save_evaluation():
    engine, path = create_test_engine()

    # Create schema
    Base.metadata.create_all(bind=engine)

    # Patch session locally
    from app.storage import SessionLocal

    original_session = SessionLocal
    SessionLocal.configure(bind=engine)

    try:
        evaluation = EvaluationResult(
            mode="professional",
            style="neutral",
            rubric_version="v1.0",
            dimensions=[
                DimensionScore(name="tone", score=8, reasoning=""),
                DimensionScore(name="structure", score=8, reasoning=""),
                DimensionScore(name="conciseness", score=8, reasoning=""),
                DimensionScore(name="actionability", score=8, reasoning=""),
                DimensionScore(name="confidence", score=8, reasoning=""),
            ],
            strengths=["Strong structure"],
            weaknesses=["None"],
            rewrite_suggestion="No changes needed.",
            rewrite_example=""
        )

        record_id = save_evaluation("Test text", evaluation)

        session = SessionLocal()
        record = session.query(EvaluationORM).filter_by(id=record_id).first()

        assert record is not None
        assert record.mode == "professional"
        assert record.computed_score == 8.0

    finally:
        SessionLocal.configure(bind=original_session.kw["bind"])
        os.unlink(path)