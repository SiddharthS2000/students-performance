from __future__ import annotations

import json
from pathlib import Path

from src.config import (
    ACTUAL_VS_PREDICTED_PLOT_PATH,
    ARTIFACTS_DIR,
    DATASET_PATH,
    EVALUATION_SUMMARY_PATH,
    METRICS_PATH,
    MODEL_PATH,
    PLOTS_DIR,
    RANDOM_SEED,
    RESIDUAL_PLOT_PATH,
)
from src.data_ingestion import load_dataset, prepare_features_and_target
from src.exception import DataValidationError, ModelArtifactError
from src.logger import get_logger

logger = get_logger(__name__)


def evaluate_model(
    dataset_path: Path = DATASET_PATH, model_path: Path = MODEL_PATH
) -> dict:
    import joblib
    import matplotlib

    matplotlib.use("Agg")

    import matplotlib.pyplot as plt
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    from sklearn.model_selection import train_test_split

    if not model_path.exists():
        raise ModelArtifactError(f"Model artifact not found at {model_path}")

    dataframe = load_dataset(dataset_path)
    features, target = prepare_features_and_target(dataframe)
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=RANDOM_SEED,
    )

    pipeline = joblib.load(model_path)
    predictions = pipeline.predict(x_test)

    metrics = {
        "mae": float(mean_absolute_error(y_test, predictions)),
        "rmse": float(_root_mean_squared_error(y_test, predictions)),
        "r2": float(r2_score(y_test, predictions)),
        "evaluation_rows": int(len(x_test)),
    }

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    with METRICS_PATH.open("w", encoding="utf-8") as metrics_file:
        json.dump(metrics, metrics_file, indent=2)

    _save_plots(y_test, predictions)
    with EVALUATION_SUMMARY_PATH.open("w", encoding="utf-8") as summary_file:
        json.dump(
            {
                **metrics,
                "residual_plot_path": str(RESIDUAL_PLOT_PATH),
                "actual_vs_predicted_plot_path": str(ACTUAL_VS_PREDICTED_PLOT_PATH),
            },
            summary_file,
            indent=2,
        )
    logger.info("Evaluation completed and saved to %s", METRICS_PATH)
    return metrics


def _save_plots(y_test, predictions) -> None:
    import matplotlib.pyplot as plt

    residuals = y_test - predictions

    plt.figure(figsize=(8, 5))
    plt.scatter(predictions, residuals, alpha=0.7)
    plt.axhline(0, color="red", linestyle="--")
    plt.xlabel("Predicted math score")
    plt.ylabel("Residual")
    plt.title("Residual Analysis")
    plt.tight_layout()
    plt.savefig(RESIDUAL_PLOT_PATH)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.scatter(y_test, predictions, alpha=0.7)
    plt.axline((0, 0), slope=1, linestyle="--")
    plt.xlabel("Actual math score")
    plt.ylabel("Predicted math score")
    plt.title("Actual vs Predicted")
    plt.tight_layout()
    plt.savefig(ACTUAL_VS_PREDICTED_PLOT_PATH)
    plt.close()


def _root_mean_squared_error(y_true, y_pred) -> float:
    from sklearn.metrics import mean_squared_error

    try:
        from sklearn.metrics import root_mean_squared_error

        return float(root_mean_squared_error(y_true, y_pred))
    except ImportError:
        return float(mean_squared_error(y_true, y_pred, squared=False))
    except TypeError:
        return float(mean_squared_error(y_true, y_pred, squared=False))


def main() -> None:
    try:
        evaluate_model()
    except (DataValidationError, ModelArtifactError) as exc:
        logger.exception("Evaluation failed")
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
