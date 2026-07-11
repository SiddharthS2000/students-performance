# Data Model: Score Prediction Platform

## Entities

### StudentRecord

- Purpose: Represents one row of student performance data from the source dataset.
- Fields:
  - `gender`: categorical, required
  - `race_ethnicity`: categorical, required
  - `parental_level_of_education`: categorical, required
  - `lunch`: categorical, required
  - `test_preparation_course`: categorical, required
  - `math_score`: integer target, required for training data and excluded from prediction input
  - `reading_score`: integer, required
  - `writing_score`: integer, required
- Validation rules:
  - Categorical fields must be non-empty strings from the allowed training vocabulary.
  - Score fields must be numeric values in the inclusive range 0 to 100.
  - The record must be complete before it enters the preprocessing pipeline.

### PredictionInput

- Purpose: Represents the user-provided feature set used to request a score prediction.
- Fields:
  - Same as `StudentRecord` except `math_score`
- Validation rules:
  - Required feature fields must be present and normalized before prediction.
  - Any echoed text must be sanitized or escaped before rendering in HTML.

### TrainingDataset

- Purpose: The prepared dataset used to train and evaluate the model.
- Fields:
  - `source_path`: dataset location
  - `rows`: collection of `StudentRecord`
  - `feature_matrix`: transformed features used by the model
  - `target_vector`: `math_score` values
- Relationships:
  - Produces one trained model artifact per successful training run.
  - Produces one evaluation summary per successful evaluation run.

### ModelArtifact

- Purpose: Serialized representation of the trained pipeline.
- Fields:
  - `artifact_path`
  - `model_name`
  - `training_timestamp`
  - `random_seed`
  - `feature_schema`
  - `version_tag`
- State transitions:
  - `created` -> `validated` -> `saved` -> `loaded_for_prediction`

### EvaluationSummary

- Purpose: Captures model performance and supporting visuals.
- Fields:
  - `mae`
  - `rmse`
  - `r2`
  - `residual_plot_path`
  - `actual_vs_predicted_plot_path`
  - `feature_inspection_plot_path`
- Relationships:
  - Linked to one `ModelArtifact` and one `TrainingDataset` split.

### PredictionResult

- Purpose: The output returned by the UI or API after scoring a request.
- Fields:
  - `predicted_math_score`
  - `input_echo`
  - `validation_messages`
  - `created_at`
- Validation rules:
  - Predictions must be numeric.
  - Input echoes must be sanitized before HTML rendering.

## Workflow States

1. Raw dataset is ingested from the read-only CSV.
2. Dataset is validated and transformed into model-ready features.
3. Model is trained and serialized as an artifact.
4. Model is evaluated and metrics are recorded.
5. Prediction requests are validated, sanitized, and scored.
