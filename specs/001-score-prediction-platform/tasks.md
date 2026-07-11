# Tasks: Score Prediction Platform

**Input**: Design documents from `/specs/001-score-prediction-platform/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Included because the feature spec defines independent test criteria for each user story.

**Organization**: Tasks are grouped by user story so each story can be implemented and tested independently.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 [P] Create the core package and artifact directories with package initializers in src/__init__.py, backend/__init__.py, backend/routes/__init__.py, backend/schemas/__init__.py, tests/unit/.gitkeep, tests/integration/.gitkeep, tests/contract/.gitkeep, and artifacts/.gitkeep
- [X] T002 [P] Add runtime and test dependencies for FastAPI, Uvicorn, scikit-learn, pandas, joblib, Jinja2, Bleach, matplotlib, seaborn, pytest, httpx, and python-multipart in requirements.txt
- [X] T003 [P] Create the container build context in Dockerfile and .dockerignore for the planned backend and artifact layout

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Repair the shared diagnostics implementation in src/logger.py and define project exception types in src/exception.py
- [X] T005 [P] Add shared file-path and runtime configuration constants in src/config.py
- [X] T006 [P] Add raw CSV ingestion and schema validation helpers in src/data_ingestion.py
- [X] T007 [P] Add reusable preprocessing and feature transformation pipeline code in src/preprocessing.py
- [X] T008 [P] Add HTML sanitization helpers for echoed text in src/sanitization.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Train the score model (Priority: P1) 🎯 MVP

**Goal**: Prepare the dataset, train the score prediction model, and persist a reusable artifact.

**Independent Test**: Running the training workflow loads the raw CSV, splits the data, trains the model, and saves a versioned artifact without manual code edits.

### Tests for User Story 1

- [X] T009 [P] [US1] Add unit tests for CSV ingestion and preprocessing in tests/unit/test_data_ingestion.py and tests/unit/test_preprocessing.py
- [X] T010 [P] [US1] Add integration coverage for the training workflow and saved artifact in tests/integration/test_model_training.py

### Implementation for User Story 1

- [X] T011 [US1] Implement the training pipeline, train/test split, fixed seed handling, and model artifact persistence in src/model_training.py
- [X] T012 [US1] Add the training entrypoint and usage documentation in README.md for running python -m src.model_training and locating the saved artifact

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Evaluate and inspect performance (Priority: P2)

**Goal**: Report model performance and create visual summaries that explain fit and error behavior.

**Independent Test**: Running the evaluation workflow against the saved model produces metrics and generated plots that can be reviewed independently of the UI.

### Tests for User Story 2

- [X] T013 [P] [US2] Add unit tests for evaluation metrics in tests/unit/test_model_evaluation.py
- [X] T014 [P] [US2] Add integration coverage for evaluation outputs and generated plots in tests/integration/test_model_evaluation_integration.py

### Implementation for User Story 2

- [X] T015 [US2] Implement regression metrics, summary serialization, and evaluation result saving in src/model_evaluation.py
- [X] T016 [US2] Implement visualization generation for residuals and actual-vs-predicted comparisons in src/model_evaluation.py
- [X] T017 [US2] Add the evaluation entrypoint and usage documentation in README.md for running python -m src.model_evaluation and locating generated reports

**Checkpoint**: At this point, User Stories 1 and 2 should both work independently

---

## Phase 5: User Story 3 - Predict scores through UI and programmatic access (Priority: P3)

**Goal**: Let users submit student input through a simple HTML interface or a programmatic request and receive a predicted score.

**Independent Test**: Submitting the same valid record through the UI and the JSON API returns a prediction response, and invalid input shows clear validation feedback.

### Tests for User Story 3

- [X] T018 [P] [US3] Add contract coverage for GET /health, GET /, POST /predict, and POST /api/predict in tests/contract/test_prediction_api.py
- [X] T019 [P] [US3] Add integration coverage for HTML form submission, API scoring, and validation feedback in tests/integration/test_prediction_ui.py

### Implementation for User Story 3

- [X] T020 [US3] Define the prediction request and response schemas in backend/schemas/prediction.py
- [X] T021 [US3] Implement model loading, artifact resolution, and inference in src/prediction.py
- [X] T022 [US3] Implement the JSON health and prediction routes in backend/routes/health.py and backend/routes/predict.py
- [X] T023 [US3] Implement the HTML form route, submit handling, and sanitized result rendering in backend/routes/pages.py
- [X] T024 [US3] Wire the FastAPI application and router registration in backend/main.py
- [X] T025 [US3] Create the prediction form and result templates in backend/templates/index.html and backend/templates/result.html
- [X] T026 [US3] Add the UI styles in backend/static/styles.css
- [X] T027 [US3] Finalize HTML sanitization behavior in src/sanitization.py and backend/routes/pages.py so echoed input is safe to render
- [X] T028 [US3] Complete the Docker launch command and runtime documentation in Dockerfile and README.md so the app starts consistently in containers

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T029 [P] Update README.md and specs/001-score-prediction-platform/quickstart.md with the validated end-to-end training, evaluation, UI, API, and Docker workflow
- [ ] T030 [P] Refactor notebooks/students-performance.ipynb and notebooks/1-EDA.ipynb to import shared helpers from src/ where notebook logic was promoted into the application
- [X] T031 [P] Run the smoke validation steps from specs/001-score-prediction-platform/quickstart.md and record any command corrections in README.md or specs/001-score-prediction-platform/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User Story 1 must land first because it creates the reusable model artifact
  - User Story 2 and User Story 3 can then proceed in parallel or sequentially, but both rely on the trained artifact from User Story 1
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2), but it consumes the trained model artifact from User Story 1
- **User Story 3 (P3)**: Can start after Foundational (Phase 2), but it consumes the trained model artifact from User Story 1

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Shared helpers before feature-specific services
- Services before endpoints or UI wiring
- Core implementation before integration
- Story complete before moving to the next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel once T004 is complete
- All tests for a user story marked [P] can run in parallel
- Different user stories can be worked on in parallel after User Story 1 is complete if the trained model artifact is already available

---

## Parallel Example: User Story 1

```bash
Task: "Add unit tests for CSV ingestion and preprocessing in tests/unit/test_data_ingestion.py and tests/unit/test_preprocessing.py"
Task: "Add integration coverage for the training workflow and saved artifact in tests/integration/test_model_training.py"
```

## Parallel Example: User Story 2

```bash
Task: "Add unit tests for evaluation metrics in tests/unit/test_model_evaluation.py"
Task: "Add integration coverage for evaluation outputs and generated plots in tests/integration/test_model_evaluation.py"
```

## Parallel Example: User Story 3

```bash
Task: "Add contract coverage for GET /health, GET /, POST /predict, and POST /api/predict in tests/contract/test_prediction_api.py"
Task: "Add integration coverage for HTML form submission, API scoring, and validation feedback in tests/integration/test_prediction_ui.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational -> Foundation ready
2. Add User Story 1 -> Test independently -> Deploy/Demo (MVP)
3. Add User Story 2 -> Test independently -> Deploy/Demo
4. Add User Story 3 -> Test independently -> Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence