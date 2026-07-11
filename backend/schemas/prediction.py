from pydantic import BaseModel, Field


class PredictionInput(BaseModel):
    gender: str = Field(..., min_length=1)
    race_ethnicity: str = Field(..., min_length=1)
    parental_level_of_education: str = Field(..., min_length=1)
    lunch: str = Field(..., min_length=1)
    test_preparation_course: str = Field(..., min_length=1)
    reading_score: float = Field(..., ge=0, le=100)
    writing_score: float = Field(..., ge=0, le=100)

    model_config = {"populate_by_name": True}


class PredictionResponse(BaseModel):
    predicted_math_score: float
    model_version: str
    validation_messages: list[str]
