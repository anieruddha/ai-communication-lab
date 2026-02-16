from sqlalchemy import (
    create_engine,
    Column,
    String,
    Text,
    Float,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import uuid, os
from app.models import EvaluationResult
from app.scoring import compute_weighted_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "evaluations.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class EvaluationORM(Base):
    __tablename__ = "evaluations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    input_text = Column(Text, nullable=False)
    suggestion_text = Column(Text, nullable=True)
    mode = Column(String, nullable=False)
    style = Column(String, nullable=False)
    rubric_version = Column(String, nullable=False)
    validated_json = Column(Text, nullable=False)
    computed_score = Column(Float, nullable=False)
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())


def init_db(custom_engine=None):
    target_engine = custom_engine or engine
    Base.metadata.create_all(bind=target_engine)

def save_evaluation(
    input_text: str,
    evaluation: EvaluationResult,
) -> str:
    session = SessionLocal()
    try:
        computed_score = compute_weighted_score(
            evaluation.mode,
            evaluation.dimensions,
        )

        record = EvaluationORM(
            input_text=input_text,
            suggestion_text=evaluation.rewrite_example,
            mode=evaluation.mode,
            style=evaluation.style,
            rubric_version=evaluation.rubric_version,
            validated_json=evaluation.model_dump_json(),
            computed_score=computed_score,
        )

        session.add(record)
        session.commit()

        return record.id

    finally:
        session.close()