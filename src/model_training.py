from __future__ import annotations

import json
from pathlib import Path

from src.config import (
    ARTIFACTS_DIR,
    DATASET_PATH,
    MODEL_METADATA_PATH,
    MODEL_PATH,
    RANDOM_SEED,
    TRAINING_SUMMARY_PATH,
)
from src.data_ingestion import load_dataset, prepare_features_and_target
from src.exception import DataValidationError, TrainingError
from src.logger import get_logger
from src.preprocessing import build_model_pipeline

logger = get_logger(__name__)


def train_model(
    dataset_path: Path = DATASET_PATH, model_path: Path = MODEL_PATH
) -> dict:
    import joblib
    import pandas as pd
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    from sklearn.model_selection import train_test_split

    dataframe = load_dataset(dataset_path)
    features, target = prepare_features_and_target(dataframe)
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=RANDOM_SEED,
    )

    pipeline = build_model_pipeline(
        RandomForestRegressor(n_estimators=200, random_state=RANDOM_SEED)
    )
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_path)

    metrics = {
        "train_rows": int(len(x_train)),
        "test_rows": int(len(x_test)),
        "model_path": str(model_path),
        "mean_prediction": float(pd.Series(predictions).mean()),
        "mae": float(mean_absolute_error(y_test, predictions)),
        "rmse": float(_root_mean_squared_error(y_test, predictions)),
        "r2": float(r2_score(y_test, predictions)),
        "random_seed": RANDOM_SEED,
    }
    with TRAINING_SUMMARY_PATH.open("w", encoding="utf-8") as summary_file:
        json.dump(metrics, summary_file, indent=2)
    with MODEL_METADATA_PATH.open("w", encoding="utf-8") as metadata_file:
        json.dump(
            {
                "model_version": "v1",
                "random_seed": RANDOM_SEED,
                "model_path": str(model_path),
                "artifact_type": "sklearn_pipeline",
            },
            metadata_file,
            indent=2,
        )

    logger.info("Model trained and saved to %s", model_path)
    return metrics


def main() -> None:
    try:
        train_model()
    except (DataValidationError, TrainingError) as exc:
        logger.exception("Training failed")
        raise SystemExit(str(exc)) from exc


def _root_mean_squared_error(y_true, y_pred) -> float:
    from sklearn.metrics import mean_squared_error

    try:
        from sklearn.metrics import root_mean_squared_error

        return float(root_mean_squared_error(y_true, y_pred))
    except ImportError:
        return float(mean_squared_error(y_true, y_pred, squared=False))
    except TypeError:
        return float(mean_squared_error(y_true, y_pred, squared=False))


if __name__ == "__main__":
    main()
