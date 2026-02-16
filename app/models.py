from pydantic import BaseModel, Field
from typing import List, Literal


ModeType = Literal["professional", "technical", "clarity"]

EvaluatorStyle = Literal[
    "neutral",
    "strict_corporate",
    "engineering_peer",
    "communication_coach",
]


class DimensionScore(BaseModel):
    name: str
    score: float = Field(ge=0, le=10)
    reasoning: str


class EvaluationResult(BaseModel):
    mode: ModeType
    style: EvaluatorStyle
    rubric_version: str
    dimensions: List[DimensionScore]
    strengths: List[str]
    weaknesses: List[str]
    rewrite_suggestion: str
    rewrite_example: str