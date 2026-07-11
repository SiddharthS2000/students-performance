<!--
Sync Impact Report
Version change: 1.0.0 -> 1.1.0
Modified principles: Notebook-First Logic, Reproducible Data Pipeline, Small, Testable Python Units,
Evidence Over Narrative, Minimal, Explicit Dependencies -> Modular ML Architecture, Reproducible
ML Workflow, Logging and Exception Discipline, Metric-Driven Evaluation, Simple UI and Deployment
Readiness
Added sections: Model, UI & Deployment Standards; Workflow & Review Gates
Removed sections: none
Templates reviewed: ✅ .specify/templates/plan-template.md, ✅ .specify/templates/spec-template.md, ✅ .specify/templates/tasks-template.md
Deferred items: none
-->

# students-performance Constitution

## Core Principles

### I. Modular ML Architecture
All reusable behavior MUST live in importable modules under `src/`. The codebase MUST separate data
loading, preprocessing, feature engineering, training, evaluation, UI adapters, and deployment
configuration into distinct modules or packages. Notebooks MAY orchestrate experiments, but they MUST
not become the primary home for production logic.

Rationale: modular boundaries keep an end-to-end ML project maintainable and testable as it grows.

### II. Reproducible ML Workflow
All dataset splits, preprocessing steps, training runs, and exported artifacts MUST be reproducible.
Randomized operations MUST use explicit seeds. Raw inputs MUST be treated as read-only, and derived
artifacts MUST be generated through documented code paths rather than edited by hand.

Rationale: reproducibility is required for credible model iteration and deployment.

### III. Logging and Exception Discipline
All non-trivial flows MUST use the shared logger and project exception types for observability and
error control. Bare prints, silent failures, and blanket exception swallowing are forbidden in source
code. Errors MUST surface with actionable messages that identify the failing stage or input.

Rationale: ML pipelines fail in data, training, inference, and UI layers; clear diagnostics are
mandatory.

### IV. Metric-Driven Evaluation
Every model claim MUST be backed by measurable evaluation. Baselines, train/validation/test splits,
and the chosen primary metric MUST be documented before implementation. Charts and tables MUST have
clear labels, and any comparison between models MUST name the dataset slice and metric used.

Rationale: model quality must be demonstrated, not asserted.

### V. Simple UI and Deployment Readiness
The user-facing surface MUST be intentionally simple, with one primary workflow and no unnecessary
screens or controls. Deployment strategy MUST be defined early, documented in the repo, and kept
compatible with the project dependencies and artifact layout. Configuration MUST be externalized and
safe to change without code edits.

Rationale: a clear UI and a documented deployment path turn an analysis project into a usable product.

## Model, UI & Deployment Standards

- Python 3 is the baseline runtime for notebooks, training code, and the UI layer.
- The repository MUST document the model training entrypoint, evaluation entrypoint, and UI entrypoint.
- Any persisted model artifact MUST be versioned or named so it can be traced back to its training
	code and data.
- If a UI is introduced, it MUST call shared source modules instead of reimplementing pipeline logic.
- Deployment targets MUST be documented with the minimum steps needed to reproduce the app locally
	and in the intended environment.
- New dependencies for model training, UI, or deployment MUST be added only when they are actually
	used.

## Data & Environment Standards

- Raw inputs under `notebooks/dataset/` are treated as read-only data sources.
- Notebook executions and training runs MUST assume a clean environment with explicitly installed
	dependencies.
- Derived files, exports, checkpoints, and figures MUST be created intentionally and stored in
	documented locations.
- Any new notebook MUST state its purpose, input data, and expected output in its opening markdown
	cell.
- Shared logging output is for diagnostics only and MUST never be required for correctness.
- Secrets, credentials, and environment-specific values MUST live outside the repository or in ignored
	configuration files.

## Workflow & Review Gates

- Any change that affects data handling, feature engineering, training, evaluation, UI behavior, or
	deployment MUST update the source file or notebook that demonstrates the behavior.
- Before a change is merged, run the smallest relevant validation available: module import, targeted
	unit check, notebook cell execution, or UI smoke test.
- Prefer incremental changes over large rewrites so data, model, and UI behavior can be reviewed and
	rerun safely.
- If logic is promoted from a notebook into `src/`, the notebook MUST import the shared helper rather
	than duplicate it.
- Breaking changes to data assumptions, model inputs, output structure, or deployment steps MUST be
	documented in the associated notebook, `README.md`, or deployment guide.
- `src/logger.py` and `src/exception.py` are the canonical shared utilities for diagnostics and
	domain failures, and all new pipeline code MUST integrate with them.

## Governance
The constitution supersedes all other project guidance when they conflict.

Amendments require a written rationale, a semantic version bump, and updates to dependent templates
or runtime guidance when the change affects them.

Versioning policy:
- MAJOR for backward-incompatible governance changes or principle removals/redefinitions.
- MINOR for new principles, new sections, or materially expanded standards.
- PATCH for clarifications, wording fixes, and other non-semantic refinements.

Compliance review expectations:
- Every spec, plan, and task document MUST be checked against this constitution.
- Any justified departure MUST be made explicit in the relevant complexity or follow-up notes.
- Reviews SHOULD confirm reproducibility, dependency discipline, and notebook/source separation.

**Version**: 1.1.0 | **Ratified**: 2026-07-06 | **Last Amended**: 2026-07-07
