"""Automated tests for the intrusion detection prototype."""

import pandas as pd
import pytest

from src.data_loader import (
    FEATURE_COLUMNS,
    load_dataset,
    split_features_target,
)
from src.predict import predict_traffic
from train_model import build_pipeline


@pytest.fixture
def trained_model():
    """Train a fresh model from the bundled synthetic dataset."""
    dataset = load_dataset()
    X, y = split_features_target(dataset)

    model = build_pipeline()
    model.fit(X, y)
    return model


def test_dataset_loads_with_expected_columns():
    dataset = load_dataset()

    assert not dataset.empty
    assert dataset.columns.tolist() == FEATURE_COLUMNS + ["label"]
    assert set(dataset["label"].unique()) == {"normal", "suspicious"}


def test_feature_target_split():
    dataset = load_dataset()
    X, y = split_features_target(dataset)

    assert X.columns.tolist() == FEATURE_COLUMNS
    assert len(X) == len(y)


def test_model_predicts_one_record(trained_model):
    dataset = load_dataset()
    record = dataset[FEATURE_COLUMNS].iloc[0].to_dict()

    predictions = predict_traffic(trained_model, record)

    assert len(predictions) == 1
    assert predictions[0] in {"normal", "suspicious"}


def test_model_predicts_multiple_records(trained_model):
    dataset = load_dataset()
    records = dataset[FEATURE_COLUMNS].head(3)

    predictions = predict_traffic(trained_model, records)

    assert len(predictions) == 3
    assert set(predictions).issubset({"normal", "suspicious"})


def test_missing_feature_is_rejected(trained_model):
    invalid_record = {
        "duration": 1,
        "protocol_type": "tcp",
    }

    with pytest.raises(ValueError, match="missing features"):
        predict_traffic(trained_model, invalid_record)


def test_wrong_input_type_is_rejected(trained_model):
    with pytest.raises(TypeError):
        predict_traffic(trained_model, "not network traffic")


def test_missing_dataset_file_is_reported(tmp_path):
    missing_path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_dataset(missing_path)


def test_model_handles_unknown_categories(trained_model):
    record = {
        "duration": 1,
        "protocol_type": "future_protocol",
        "service": "unknown_service",
        "flag": "unknown_flag",
        "src_bytes": 10,
        "dst_bytes": 20,
        "count": 1,
        "same_srv_rate": 0.5,
        "error_rate": 0.0,
    }

    predictions = predict_traffic(trained_model, record)

    assert len(predictions) == 1
    assert predictions[0] in {"normal", "suspicious"}


def test_missing_values_are_rejected(trained_model):
    record = {
        "duration": 1,
        "protocol_type": "tcp",
        "service": "http",
        "flag": "normal",
        "src_bytes": 100,
        "dst_bytes": 200,
        "count": 2,
        "same_srv_rate": 0.8,
        "error_rate": None,
    }

    with pytest.raises(ValueError, match="missing values"):
        predict_traffic(trained_model, record)
