# Research Notes: Score Prediction Platform

## 1. Prediction target and modeling approach

- Decision: Predict `math score` as the primary target using a scikit-learn pipeline with `ColumnTransformer`, categorical encoding, and a regression estimator.
- Rationale: The existing notebooks already treat `math score` as the held-out target in their model-building section, and the dataset has a mixed numeric/categorical structure that fits a pipeline-based tabular regression workflow.
- Alternatives considered: Predicting a combined score or another subject score was considered, but that would diverge from the notebook pattern and complicate the initial delivery.

## 2. Backend and UI stack

- Decision: Use FastAPI for the backend and server-rendered HTML/CSS for the user interface.
- Rationale: FastAPI satisfies the required REST API layer, integrates cleanly with Pydantic validation, and can also serve a simple form-driven UI through templates.
- Alternatives considered: Flask was considered for simplicity, but FastAPI better matches the requested API-first shape and gives clearer request/response contracts.

## 3. Input validation and HTML sanitization

- Decision: Validate all structured inputs on the backend and sanitize any user-supplied text before rendering it back into HTML using explicit sanitization plus template escaping.
- Rationale: The feature requires a simple UI while also calling out HTML sanitization for security; defense in depth prevents reflected HTML from reaching the browser.
- Alternatives considered: Relying only on template auto-escaping was considered, but explicit sanitization is a better fit for the stated security requirement.

## 4. Artifact storage and deployment

- Decision: Store trained model files, evaluation outputs, and other generated artifacts on disk under `artifacts/`, then package the app in a single Docker image.
- Rationale: A file-based artifact layout keeps the demo reproducible, easy to inspect, and aligned with the repository’s lightweight ML workflow.
- Alternatives considered: Adding a database or object store was rejected because the project scope is a single-model local application.

## 5. Evaluation and testing strategy

- Decision: Use regression metrics such as MAE, RMSE, and R², plus visualizations for error and feature inspection; validate with pytest, FastAPI TestClient, and a Docker smoke test.
- Rationale: The constitution requires metric-driven evaluation and the plan needs a practical way to verify both the training pipeline and the user-facing app.
- Alternatives considered: Notebook-only validation was rejected because the feature includes API and HTML delivery paths that need explicit automated checks.

## 6. Model choice

- Decision: Use a scikit-learn regression model with a strong baseline and keep the exact estimator swappable behind the same pipeline contract.
- Rationale: The notebook pattern already uses scikit-learn preprocessing, and a pipeline boundary keeps the implementation maintainable if model selection changes later.
- Alternatives considered: A pure linear model is simpler, but a more flexible tabular regressor is usually a better first production-style candidate for mixed student features.