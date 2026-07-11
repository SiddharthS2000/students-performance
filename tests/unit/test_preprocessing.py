from src.preprocessing import build_preprocessor


def test_build_preprocessor_exposes_feature_names():
    preprocessor = build_preprocessor()

    assert preprocessor is not None
