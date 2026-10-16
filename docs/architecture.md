# System Architecture

## 1. Project Overview

The AI-Based Network Intrusion Detection System is an educational machine-learning prototype that classifies network traffic records into two categories:

- `normal`
- `suspicious`

The project uses synthetic sample records to demonstrate the machine-learning workflow. It does not capture live network traffic or provide production-grade security monitoring.

## 2. Architecture Diagram

```text
Synthetic CSV Dataset
        |
        v
src/data_loader.py
        |
        v
Feature and Label Separation
        |
        v
train_model.py
        |
        v
Preprocessing Pipeline
  - One-Hot Encoding
  - Numeric Features
        |
        v
Random Forest Classifier
        |
        v
models/intrusion_model.joblib
        |
        v
src/predict.py
        |
        v
app.py (Streamlit Dashboard)
        |
        v
Normal / Suspicious Prediction
```

## 3. Main Components

### Dataset

File: `data/sample_network_traffic.csv`

Contains synthetic traffic records, including protocol, service, connection flag, byte counts, and rate features.

### Data Loader

File: `src/data_loader.py`

Responsibilities:

- Load the CSV dataset.
- Validate required columns and target labels.
- Check missing values and numeric ranges.
- Separate model features from target labels.

### Model Training

File: `train_model.py`

Responsibilities:

- Split data into training and test subsets.
- Encode categorical features.
- Train a Random Forest classifier.
- Print classification metrics.
- Save the fitted pipeline.

### Prediction Module

File: `src/predict.py`

Responsibilities:

- Load the saved model.
- Validate prediction input columns.
- Generate predictions for one or more records.

### Dashboard

File: `app.py`

Responsibilities:

- Display the sample dataset.
- Show the label distribution.
- Accept traffic feature values.
- Display the model prediction.

### Automated Tests

File: `tests/test_prediction.py`

Checks data loading, feature separation, model predictions, missing inputs, and unknown categories.

## 4. Input Features

| Feature | Description |
|---|---|
| `duration` | Connection duration |
| `protocol_type` | Protocol category |
| `service` | Service category |
| `flag` | Connection status category |
| `src_bytes` | Bytes sent from source |
| `dst_bytes` | Bytes sent to destination |
| `count` | Connection count feature |
| `same_srv_rate` | Same-service rate |
| `error_rate` | Error rate |

The values are illustrative features for this prototype, not a complete or validated network traffic specification.

## 5. Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Train the model:

```bash
python train_model.py
```

Run automated tests:

```bash
python -m pytest -v
```

Launch the dashboard:

```bash
streamlit run app.py
```

## 6. Limitations

- The included dataset is small and synthetic.
- The model may learn artificial patterns in the sample data.
- Accuracy on synthetic data does not establish real-world performance.
- The system does not capture packets or monitor a live network.
- Predictions must not be used as the sole basis for security decisions.

## 7. Future Improvements

- Evaluate against a reputable public intrusion-detection dataset.
- Add more robust validation and class-imbalance analysis.
- Report precision, recall, F1-score, and confusion matrix.
- Add reproducible experiments and continuous integration.
- Explore live traffic integration only in an authorized test environment.
