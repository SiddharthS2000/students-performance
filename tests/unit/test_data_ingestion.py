from pathlib import Path

import pandas as pd
import pytest

from src.data_ingestion import (
    load_dataset,
    prepare_features_and_target,
    validate_dataset,
)
from src.exception import DataValidationError


def test_load_dataset_returns_dataframe():
    dataframe = load_dataset(Path("notebooks/dataset/StudentsPerformance.csv"))

    assert not dataframe.empty
    assert "math score" in dataframe.columns


def test_validate_dataset_rejects_missing_column():
    dataframe = pd.DataFrame({"gender": ["female"], "math score": [72]})

    with pytest.raises(DataValidationError):
        validate_dataset(dataframe)


def test_prepare_features_and_target_returns_expected_shapes():
    dataframe = load_dataset(Path("notebooks/dataset/StudentsPerformance.csv"))

    features, target = prepare_features_and_target(dataframe)

    assert list(features.columns) == [
        "gender",
        "race/ethnicity",
        "parental level of education",
        "lunch",
        "test preparation course",
        "reading score",
        "writing score",
    ]
    assert len(features) == len(target)
