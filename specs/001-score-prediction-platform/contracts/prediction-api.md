# Prediction API Contract

## Overview

The service exposes a browser-facing HTML prediction form and a JSON API for programmatic scoring. Both paths use the same trained model and the same validation rules.

## Endpoints

### GET /health

Purpose: Liveness check for the service.

Response:

```json
{
  "status": "ok"
}
```

### GET /

Purpose: Render the HTML prediction form.

Response: HTML document containing a single prediction form.

### POST /predict

Purpose: Accept form-submitted input from the UI and render a prediction result page.

Request format: form fields matching `PredictionInput`.

Response: HTML result page containing the predicted math score and any validation messages.

### POST /api/predict

Purpose: Accept JSON input for programmatic score prediction.

Request JSON:

```json
{
  "gender": "female",
  "race_ethnicity": "group C",
  "parental_level_of_education": "some college",
  "lunch": "standard",
  "test_preparation_course": "completed",
  "reading_score": 90,
  "writing_score": 88
}
```

Success response JSON:

```json
{
  "predicted_math_score": 87.4,
  "model_version": "v1",
  "validation_messages": []
}
```

Validation error response JSON:

```json
{
  "detail": [
    {
      "field": "reading_score",
      "message": "Must be between 0 and 100"
    }
  ]
}
```

## Input Rules

- All categorical values must be present and non-empty.
- Numeric scores must be integers or numeric values within 0 to 100.
- Any text echoed into HTML must be sanitized or escaped before rendering.

## Output Rules

- Predictions must be numeric.
- API responses must be machine-readable JSON.
- UI responses must be human-readable and must not expose raw HTML from user input.
