from pathlib import Path

from src.config import MODEL_PATH
from src.model_training import train_model


def test_training_creates_model_artifact(tmp_path, monkeypatch):
    model_path = tmp_path / "model.joblib"

    metrics = train_model(model_path=model_path)

    assert model_path.exists()
    assert metrics["train_rows"] > 0
    assert metrics["test_rows"] > 0
