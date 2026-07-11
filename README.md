# students-performance

## Score Prediction Platform

This project trains a student math-score model, evaluates it, and serves predictions through both a browser UI and a JSON API.

## Local Workflow

Activate your Python environment, install dependencies, then run the workflow steps below.

```bash
python -m src.model_training
python -m src.model_evaluation
uvicorn backend.main:app --reload
```

Expected artifacts:

- `artifacts/model.joblib`
- `artifacts/training_summary.json`
- `artifacts/metrics.json`
- `artifacts/evaluation_summary.json`
- `artifacts/plots/residuals.png`
- `artifacts/plots/actual_vs_predicted.png`

## Docker

Build and run the container with:

```bash
docker build -t students-performance .
docker run --rm -p 8000:8000 students-performance
```

## Validation

Run the test suite with:

```bash
pytest -q
```