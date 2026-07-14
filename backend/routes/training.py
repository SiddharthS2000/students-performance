from __future__ import annotations

import json

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse


from backend.schemas.training import TrainingResponse
from backend.templates_env import templates
from src.config import (
    DEFAULT_MODEL_VERSION,
    TRAINING_PLOT_PATH,
    TRAINING_SUMMARY_PATH,
    EVALUATION_SUMMARY_PATH,
    ACTUAL_VS_PREDICTED_PLOT_PATH,
    RESIDUAL_PLOT_PATH,
)
from src.exception import DataValidationError, TrainingError
from src.model_training import train_model
from src.model_evaluation import evaluate_model

router = APIRouter()


def _load_training_summary() -> dict | None:
    if not TRAINING_SUMMARY_PATH.exists():
        return None

    with TRAINING_SUMMARY_PATH.open("r", encoding="utf-8") as summary_file:
        return json.load(summary_file)


def _load_evaluation_summary() -> dict | None:
    if not EVALUATION_SUMMARY_PATH.exists():
        return None

    with EVALUATION_SUMMARY_PATH.open("r", encoding="utf-8") as summary_file:
        return json.load(summary_file)


@router.get("/train_and_evaluate", response_class=HTMLResponse)
def training_page(request: Request) -> HTMLResponse:
    training_summary = _load_training_summary()
    evaluation_summary = _load_evaluation_summary()
    return templates.TemplateResponse(
        request,
        "training.html",
        {
            "training_message": "Ready to train the model.",
            "training_summary": training_summary,
            "training_plot_url": (
                TRAINING_PLOT_PATH.name if TRAINING_PLOT_PATH.exists() else None
            ),
            "evaluation_summary": evaluation_summary,
            "actual_vs_predicted_plot_url": (
                ACTUAL_VS_PREDICTED_PLOT_PATH.name
                if ACTUAL_VS_PREDICTED_PLOT_PATH.exists()
                else None
            ),
            "residual_plot_path_url": (
                RESIDUAL_PLOT_PATH.name if RESIDUAL_PLOT_PATH.exists() else None
            ),
        },
    )


@router.post("/train_and_evaluate", response_class=HTMLResponse)
def run_training(request: Request) -> HTMLResponse:
    try:
        training_metrics = train_model()
        evaluation_metrics = evaluate_model()
        message = "Training and evaluation completed successfully."
    except (DataValidationError, TrainingError) as exc:
        training_metrics = None
        evaluation_metrics = None
        message = str(exc)

    training_summary = (
        _load_training_summary() if training_metrics is not None else None
    )
    evaluation_summary = (
        _load_evaluation_summary() if evaluation_metrics is not None else None
    )
    return templates.TemplateResponse(
        request,
        "training.html",
        {
            "training_message": message,
            "training_summary": training_summary or training_metrics,
            "training_plot_url": (
                TRAINING_PLOT_PATH.name if TRAINING_PLOT_PATH.exists() else None
            ),
            "evaluation_summary": evaluation_summary or evaluation_metrics,
            "actual_vs_predicted_plot_url": (
                ACTUAL_VS_PREDICTED_PLOT_PATH.name
                if ACTUAL_VS_PREDICTED_PLOT_PATH.exists()
                else None
            ),
            "residual_plot_path_url": RESIDUAL_PLOT_PATH,
        },
    )


@router.post("/api/train_and_evaluate", response_model=TrainingResponse)
def api_train() -> TrainingResponse:
    try:
        training_metrics = train_model()
        evaluation_metrics = evaluate_model()
        return TrainingResponse(
            status="completed",
            model_version=DEFAULT_MODEL_VERSION,
            training_metrics=training_metrics,
            validation_messages=[],
            training_plot_url=(
                TRAINING_PLOT_PATH.name if TRAINING_PLOT_PATH.exists() else None
            ),
            evaluation_metrics=evaluation_metrics,
            actual_vs_predicted_plot_url=(
                ACTUAL_VS_PREDICTED_PLOT_PATH.name
                if ACTUAL_VS_PREDICTED_PLOT_PATH.exists()
                else None
            ),
            residual_plot_path_url=(
                RESIDUAL_PLOT_PATH.name if RESIDUAL_PLOT_PATH.exists() else None
            ),
        )
    except DataValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except TrainingError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
