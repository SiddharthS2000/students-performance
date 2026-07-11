from src.model_evaluation import evaluate_model
from src.model_training import train_model


def test_evaluation_returns_core_metrics(tmp_path):
    model_path = tmp_path / "model.joblib"
    train_model(model_path=model_path)

    metrics = evaluate_model(model_path=model_path)

    assert set(metrics) >= {"mae", "rmse", "r2"}
