from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from backend.templates_env import templates
from src.config import (
    DEFAULT_MODEL_VERSION,
    FEATURE_COLUMNS,
    GENDER_OPTIONS,
    LUNCH_OPTIONS,
    PARENTAL_LEVEL_OF_EDUCATION_OPTIONS,
    RACE_ETHNICITY_OPTIONS,
    TEST_PREPARATION_OPTIONS,
)
from src.exception import ModelArtifactError, PredictionError
from src.prediction import predict_score
from src.sanitization import sanitize_text

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "fields": FEATURE_COLUMNS,
            "gender_options": GENDER_OPTIONS,
            "race_ethnicity_options": RACE_ETHNICITY_OPTIONS,
            "parental_level_of_education_options": PARENTAL_LEVEL_OF_EDUCATION_OPTIONS,
            "lunch_options": LUNCH_OPTIONS,
            "test_preparation_options": TEST_PREPARATION_OPTIONS,
        },
    )


@router.post("/predict", response_class=HTMLResponse)
def predict_page(
    request: Request,
    gender: str = Form(...),
    race_ethnicity: str = Form(...),
    parental_level_of_education: str = Form(...),
    lunch: str = Form(...),
    test_preparation_course: str = Form(...),
    reading_score: float = Form(...),
    writing_score: float = Form(...),
) -> HTMLResponse:
    payload = {
        "gender": sanitize_text(gender),
        "race/ethnicity": sanitize_text(race_ethnicity),
        "parental level of education": sanitize_text(parental_level_of_education),
        "lunch": sanitize_text(lunch),
        "test preparation course": sanitize_text(test_preparation_course),
        "reading score": reading_score,
        "writing score": writing_score,
    }

    try:
        prediction = predict_score(payload)
        message = f"Predicted math score: {prediction:.2f}"
    except (ModelArtifactError, PredictionError) as exc:
        message = str(exc)

    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "prediction_message": message,
            "sanitized_values": payload,
            "model_version": DEFAULT_MODEL_VERSION,
        },
    )
