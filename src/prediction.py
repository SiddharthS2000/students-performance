from __future__ import annotations

from pathlib import Path

from src.config import FEATURE_COLUMNS, MODEL_PATH
from src.exception import ModelArtifactError, PredictionError
from src.logger import get_logger

logger = get_logger(__name__)


def load_model(model_path: Path = MODEL_PATH):
    import joblib

    if not model_path.exists():
        raise ModelArtifactError(f"Model artifact not found at {model_path}")
    return joblib.load(model_path)


def predict_score(payload: dict, model_path: Path = MODEL_PATH) -> float:
    import pandas as pd

    model = load_model(model_path)
    frame = pd.DataFrame([payload], columns=FEATURE_COLUMNS)

    try:
        prediction = model.predict(frame)[0]
    except Exception as exc:  # pragma: no cover - protective adapter
        raise PredictionError("Prediction failed") from exc

    logger.info("Generated prediction")
    return float(prediction)
