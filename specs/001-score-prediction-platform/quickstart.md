# Quickstart: Score Prediction Platform

## Prerequisites

- Python 3.x installed
- Docker installed for container validation
- The project dependencies installed from `requirements.txt`

## Local Validation Flow

1. Install dependencies.

```bash
pip install -r requirements.txt
```

2. Run the training entrypoint.

```bash
python -m src.model_training
```

3. Run the evaluation entrypoint.

```bash
python -m src.model_evaluation
```

4. Start the web application.

```bash
uvicorn backend.main:app --reload
```

5. Open the UI in a browser and submit one valid student input record.

Expected outcome: the page returns a predicted math score and displays a clean result view.

6. Call the API with the same input using JSON.

Expected outcome: the JSON response returns the same prediction value and validation metadata.

7. Run the automated checks.

```bash
pytest -q
```

Expected outcome: the suite passes and the training, evaluation, and UI/API tests all execute successfully.

## Docker Validation Flow

1. Build the container image.

```bash
docker build -t students-performance .
```

2. Run the container locally.

```bash
docker run --rm -p 8000:8000 students-performance
```

Expected outcome: the application is reachable on `http://127.0.0.1:8000` and the prediction workflow works the same way as the local run.

## Verification Checklist

- Training creates a reusable model artifact under `artifacts/`
- Evaluation emits metrics and visual outputs
- UI form submissions are sanitized and rendered safely
- API requests return structured prediction responses
- Docker build and run complete without manual file edits
