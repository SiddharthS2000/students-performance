from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "notebooks" / "dataset" / "StudentsPerformance.csv"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
LOGS_DIR = ARTIFACTS_DIR / "logs"
PLOTS_DIR = ARTIFACTS_DIR / "plots"
MODEL_PATH = ARTIFACTS_DIR / "model.joblib"
MODEL_METADATA_PATH = ARTIFACTS_DIR / "model_metadata.json"
TRAINING_SUMMARY_PATH = ARTIFACTS_DIR / "training_summary.json"
METRICS_PATH = ARTIFACTS_DIR / "metrics.json"
EVALUATION_SUMMARY_PATH = ARTIFACTS_DIR / "evaluation_summary.json"
RANDOM_SEED = 42
DEFAULT_MODEL_VERSION = "v1"
TARGET_COLUMN = "math score"
FEATURE_COLUMNS = [
    "gender",
    "race/ethnicity",
    "parental level of education",
    "lunch",
    "test preparation course",
    "reading score",
    "writing score",
]
CATEGORICAL_COLUMNS = [
    "gender",
    "race/ethnicity",
    "parental level of education",
    "lunch",
    "test preparation course",
]
NUMERIC_COLUMNS = ["reading score", "writing score"]

GENDER_OPTIONS = ("female", "male")
RACE_ETHNICITY_OPTIONS = ("group A", "group B", "group C", "group D", "group E")
PARENTAL_LEVEL_OF_EDUCATION_OPTIONS = (
    "some high school",
    "high school",
    "some college",
    "associate's degree",
    "bachelor's degree",
    "master's degree",
)
LUNCH_OPTIONS = ("standard", "free/reduced")
TEST_PREPARATION_OPTIONS = ("none", "completed")
