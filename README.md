# 🛡️ AI-Based Network Intrusion Detection System

An educational machine-learning project that classifies sample network traffic records as **Normal** or **Suspicious** using Python, scikit-learn, and Streamlit.

> **Disclaimer:** This repository uses a small synthetic dataset for demonstration. Its predictions are not validated for real-world intrusion detection or security decisions.

## ✨ Features

- Synthetic network traffic dataset
- Data validation and feature separation
- Random Forest classification pipeline
- Categorical feature encoding
- Saved model for repeated predictions
- Interactive Streamlit dashboard
- Automated tests using pytest

## 🧰 Technology Stack

- Python
- pandas
- scikit-learn
- Streamlit
- Joblib
- pytest

## 📁 Project Structure

```text
ai-network-intrusion-detection/
├── app.py
├── train_model.py
├── requirements.txt
├── README.md
├── .gitignore
├── src/
│   ├── data_loader.py
│   └── predict.py
├── data/
│   └── sample_network_traffic.csv
├── models/
├── tests/
│   └── test_prediction.py
└── docs/
    └── architecture.md
```

## 🚀 Getting Started

### 1. Clone the repository

Replace `YOUR_USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR_USERNAME/ai-network-intrusion-detection.git
cd ai-network-intrusion-detection
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Train the model

```bash
python train_model.py
```

The trained model is saved to:

`models/intrusion_model.joblib`

### 5. Run automated tests

```bash
python -m pytest -v
```

### 6. Launch the dashboard

```bash
python -m streamlit run app.py
```

## 📊 Input Features

| Feature | Description |
|---|---|
| `duration` | Connection duration |
| `protocol_type` | Network protocol category |
| `service` | Service category |
| `flag` | Connection status category |
| `src_bytes` | Source byte count |
| `dst_bytes` | Destination byte count |
| `count` | Connection count feature |
| `same_srv_rate` | Same-service rate |
| `error_rate` | Error rate |

## 🧠 Machine Learning Workflow

1. Load and validate the dataset.
2. Separate features and target labels.
3. Split data into training and testing subsets.
4. Encode categorical features.
5. Train a Random Forest classifier.
6. Evaluate the model on the held-out subset.
7. Save the fitted pipeline and use it for predictions.

## ⚠️ Limitations

- The dataset is small and synthetic.
- Evaluation metrics are not evidence of real-world performance.
- The application does not capture live network packets.
- Predictions can be incorrect and must not be treated as proof of malicious activity.

## 🔮 Future Improvements

- Evaluate with a reputable public intrusion-detection dataset.
- Add confusion-matrix and per-class performance visualizations.
- Improve validation using larger, more representative datasets.
- Add a continuous integration workflow.
- Explore authorized live-network testing.

## 👩‍💻 Learning Objectives

This project demonstrates data validation, machine-learning pipelines, classification, model persistence, automated testing, and dashboard development.

## 📄 License

Add a license file if you intend to distribute or reuse this project publicly.
