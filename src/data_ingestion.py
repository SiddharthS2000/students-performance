from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from src.config import DATASET_PATH, FEATURE_COLUMNS, NUMERIC_COLUMNS, TARGET_COLUMN
from src.exception import DataValidationError
from src.logger import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
    import pandas as pd


def load_dataset(dataset_path: Path = DATASET_PATH) -> pd.DataFrame:
    import pandas as pd

    if not dataset_path.exists():
        raise DataValidationError(f"Dataset not found at {dataset_path}")

    logger.info("Loading dataset from %s", dataset_path)
    dataframe = pd.read_csv(dataset_path)
    validate_dataset(dataframe)
    return dataframe


def validate_dataset(dataframe: pd.DataFrame) -> None:
    import pandas as pd

    required_columns = FEATURE_COLUMNS + [TARGET_COLUMN]
    missing_columns = [
        column for column in required_columns if column not in dataframe.columns
    ]
    if missing_columns:
        raise DataValidationError(
            f"Dataset is missing required columns: {missing_columns}"
        )

    if dataframe[required_columns].isnull().any().any():
        raise DataValidationError("Dataset contains missing values in required columns")

    for column in NUMERIC_COLUMNS + [TARGET_COLUMN]:
        numeric_series = pd.to_numeric(dataframe[column], errors="coerce")
        if numeric_series.isnull().any():
            raise DataValidationError(f"Column '{column}' contains non-numeric values")
        if ((numeric_series < 0) | (numeric_series > 100)).any():
            raise DataValidationError(
                f"Column '{column}' contains values outside the 0-100 range"
            )


def prepare_features_and_target(
    dataframe: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    validate_dataset(dataframe)
    features = dataframe[FEATURE_COLUMNS].copy()
    for column in NUMERIC_COLUMNS:
        features[column] = features[column].astype(float)
    target = dataframe[TARGET_COLUMN].astype(float).copy()
    return features, target
