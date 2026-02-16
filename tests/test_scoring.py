import pytest
from app.models import DimensionScore
from app.scoring import compute_weighted_score


def test_professional_score_calculation():
    dimensions = [
        DimensionScore(name="tone", score=8, reasoning=""),
        DimensionScore(name="structure", score=9, reasoning=""),
        DimensionScore(name="conciseness", score=7, reasoning=""),
        DimensionScore(name="actionability", score=8, reasoning=""),
        DimensionScore(name="confidence", score=6, reasoning=""),
    ]

    score = compute_weighted_score("professional", dimensions)

    assert isinstance(score, float)
    assert 0 <= score <= 10


def test_missing_dimension():
    dimensions = [
        DimensionScore(name="tone", score=8, reasoning=""),
    ]

    with pytest.raises(ValueError):
        compute_weighted_score("professional", dimensions)