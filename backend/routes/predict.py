from fastapi import APIRouter, HTTPException

from backend.schemas.prediction import PredictionInput, PredictionResponse
from src.config import DEFAULT_MODEL_VERSION
from src.exception import ModelArtifactError, PredictionError
from src.prediction import predict_score

router = APIRouter()


@router.post("/api/predict", response_model=PredictionResponse)
def api_predict(payload: PredictionInput) -> PredictionResponse:
    try:
        prediction = predict_score(
            {
                "gender": payload.gender,
                "race/ethnicity": payload.race_ethnicity,
                "parental level of education": payload.parental_level_of_education,
                "lunch": payload.lunch,
                "test preparation course": payload.test_preparation_course,
                "reading score": payload.reading_score,
                "writing score": payload.writing_score,
            }
        )
        return PredictionResponse(
            predicted_math_score=prediction,
            model_version=DEFAULT_MODEL_VERSION,
            validation_messages=[],
        )
    except ModelArtifactError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except PredictionError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
