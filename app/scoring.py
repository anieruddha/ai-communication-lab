from typing import Dict
from typing import List
from app.models import DimensionScore

PROFESSIONAL_WEIGHTS: Dict[str, float] = {
    "tone": 0.25,
    "structure": 0.25,
    "conciseness": 0.20,
    "actionability": 0.20,
    "confidence": 0.10,
}

TECHNICAL_WEIGHTS: Dict[str, float] = {
    "accuracy": 0.30,
    "depth": 0.20,
    "structure": 0.20,
    "precision": 0.20,
    "assumptions": 0.10,
}

CLARITY_WEIGHTS: Dict[str, float] = {
    "readability": 0.25,
    "coherence": 0.25,
    "ambiguity": 0.20,
    "redundancy": 0.15,
    "vocabulary": 0.15,
}


def get_weights_for_mode(mode: str) -> Dict[str, float]:
    if mode == "professional":
        return PROFESSIONAL_WEIGHTS
    elif mode == "technical":
        return TECHNICAL_WEIGHTS
    elif mode == "clarity":
        return CLARITY_WEIGHTS
    else:
        raise ValueError(f"Unknown mode: {mode}")

def validate_weights(weights: Dict[str, float]) -> None:
    total = sum(weights.values())
    if round(total, 5) != 1.0:
        raise ValueError(f"Weights must sum to 1.0, got {total}")

for weight_map in (
    PROFESSIONAL_WEIGHTS,
    TECHNICAL_WEIGHTS,
    CLARITY_WEIGHTS,
): validate_weights(weight_map)


def compute_weighted_score(
    mode: str,
    dimensions: List[DimensionScore],
) -> float:
    weights = get_weights_for_mode(mode)

    score_map = {d.name: d.score for d in dimensions}

    # Ensure no missing dimensions
    for required in weights.keys():
        if required not in score_map:
            raise ValueError(f"Missing dimension: {required}")

    # Ensure no extra dimensions
    for provided in score_map.keys():
        if provided not in weights:
            raise ValueError(f"Unexpected dimension: {provided}")

    total = 0.0
    for dim, weight in weights.items():
        total += score_map[dim] * weight

    return round(total, 2)