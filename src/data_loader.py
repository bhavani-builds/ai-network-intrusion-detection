"""Load and validate the network traffic dataset."""

from pathlib import Path

import pandas as pd

FEATURE_COLUMNS = [
    "duration",
    "protocol_type",
    "service",
    "flag",
    "src_bytes",
    "dst_bytes",
    "count",
    "same_srv_rate",
    "error_rate",
]

TARGET_COLUMN = "label"
VALID_LABELS = {"normal", "suspicious"}


def load_dataset(path=None):
    """Load the CSV and validate its schema and contents."""
    if path is None:
        path = (
            Path(__file__).resolve().parents[1]
            / "data"
            / "sample_network_traffic.csv"
        )
    else:
        path = Path(path)

    if not path.is_file():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path)

    expected_columns = FEATURE_COLUMNS + [TARGET_COLUMN]
    missing = [column for column in expected_columns if column not in df.columns]

    if missing:
        raise ValueError(f"Dataset is missing columns: {missing}")

    df = df[expected_columns].copy()

    if df.empty:
        raise ValueError("Dataset contains no records.")

    if df.isnull().any().any():
        raise ValueError("Dataset contains missing values.")

    if not df[TARGET_COLUMN].isin(VALID_LABELS).all():
        raise ValueError(
            f"Labels must be one of: {sorted(VALID_LABELS)}"
        )

    numeric_columns = [
        "duration",
        "src_bytes",
        "dst_bytes",
        "count",
        "same_srv_rate",
        "error_rate",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="raise")

    if (df[numeric_columns] < 0).any().any():
        raise ValueError("Numeric features cannot be negative.")

    for column in ["same_srv_rate", "error_rate"]:
        if (df[column] > 1).any():
            raise ValueError(f"{column} must be between 0 and 1.")

    categorical_columns = ["protocol_type", "service", "flag"]

    for column in categorical_columns:
        if df[column].astype(str).str.strip().eq("").any():
            raise ValueError(f"{column} cannot contain empty values.")

    return df


def split_features_target(df):
    """Separate input features from the target labels."""
    missing = [
        column
        for column in FEATURE_COLUMNS + [TARGET_COLUMN]
        if column not in df.columns
    ]

    if missing:
        raise ValueError(f"DataFrame is missing columns: {missing}")

    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].copy()

    return X, y
