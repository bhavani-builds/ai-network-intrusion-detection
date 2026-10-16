"""Train and evaluate the network intrusion detection model."""

from pathlib import Path

import joblib
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from src.data_loader import (
    FEATURE_COLUMNS,
    load_dataset,
    split_features_target,
)


ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "models" / "intrusion_model.joblib"

CATEGORICAL_FEATURES = ["protocol_type", "service", "flag"]
NUMERIC_FEATURES = [
    "duration",
    "src_bytes",
    "dst_bytes",
    "count",
    "same_srv_rate",
    "error_rate",
]


def build_pipeline():
    """Build a reproducible preprocessing and classification pipeline."""
    preprocessing = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_FEATURES,
            ),
            ("numeric", "passthrough", NUMERIC_FEATURES),
        ]
    )

    classifier = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced",
    )

    return Pipeline(
        steps=[
            ("preprocessing", preprocessing),
            ("classifier", classifier),
        ]
    )


def main():
    df = load_dataset()
    X, y = split_features_target(df)

    if list(X.columns) != FEATURE_COLUMNS:
        raise ValueError("Unexpected feature order.")

    if y.nunique() < 2:
        raise ValueError("Training requires at least two target classes.")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.30,
        random_state=42,
        stratify=y,
    )

    model = build_pipeline()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print(f"Training records: {len(X_train)}")
    print(f"Test records: {len(X_test)}")
    print(f"Test accuracy: {accuracy_score(y_test, predictions):.3f}")
    print(
        classification_report(
            y_test,
            predictions,
            labels=["normal", "suspicious"],
            zero_division=0,
        )
    )

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
