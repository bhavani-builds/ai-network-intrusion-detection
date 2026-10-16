"""Prediction utilities for the network intrusion detection model."""

from pathlib import Path

import joblib
import pandas as pd

from src.data_loader import FEATURE_COLUMNS


DEFAULT_MODEL_PATH = (
    Path(__file__).resolve().parents[1] / "models" / "intrusion_model.joblib"
)


def load_model(model_path=None):
    """Load a previously trained model pipeline."""
    path = Path(model_path) if model_path is not None else DEFAULT_MODEL_PATH

    if not path.is_file():
        raise FileNotFoundError(
            f"Trained model not found at {path}. Run train_model.py first."
        )

    return joblib.load(path)


def predict_traffic(model, traffic):
    """Predict labels for one record or a DataFrame of records."""
    if isinstance(traffic, dict):
        traffic = pd.DataFrame([traffic])
    elif not isinstance(traffic, pd.DataFrame):
        raise TypeError("traffic must be a dictionary or pandas DataFrame")

    missing = [column for column in FEATURE_COLUMNS if column not in traffic.columns]
    if missing:
        raise ValueError(f"Traffic data is missing features: {missing}")

    features = traffic[FEATURE_COLUMNS].copy()

    if features.isnull().any().any():
        raise ValueError("Traffic features cannot contain missing values.")

    predictions = model.predict(features)

    return predictions.tolist()
