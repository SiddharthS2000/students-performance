from __future__ import annotations

from typing import TYPE_CHECKING

from src.config import CATEGORICAL_COLUMNS, NUMERIC_COLUMNS

if TYPE_CHECKING:
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline


def _make_encoder():
    from sklearn.preprocessing import OneHotEncoder

    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def build_preprocessor() -> ColumnTransformer:
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import StandardScaler

    return ColumnTransformer(
        transformers=[
            ("categorical", _make_encoder(), CATEGORICAL_COLUMNS),
            ("numeric", StandardScaler(), NUMERIC_COLUMNS),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )


def build_model_pipeline(estimator) -> Pipeline:
    from sklearn.pipeline import Pipeline

    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("model", estimator),
        ]
    )


def get_transformed_feature_names(preprocessor: ColumnTransformer) -> list[str]:
    return list(preprocessor.get_feature_names_out())
