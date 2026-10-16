"""Streamlit dashboard for the network intrusion detection prototype."""

import streamlit as st

from src.data_loader import load_dataset
from src.predict import load_model, predict_traffic


st.set_page_config(
    page_title="AI Network Intrusion Detection",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ AI-Based Network Intrusion Detection System")
st.write(
    "Explore sample network traffic and classify a record using a trained "
    "machine-learning model."
)

st.warning(
    "Educational prototype: the included dataset is synthetic and is not "
    "suitable for real-world security decisions."
)

with st.sidebar:
    st.header("About")
    st.write("Model: Random Forest classifier")
    st.write("Classes: Normal and Suspicious")
    st.write("Input: Network traffic features")

try:
    dataset = load_dataset()
except (FileNotFoundError, ValueError) as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.stop()

left, right = st.columns(2)

with left:
    st.subheader("Sample dataset")
    st.dataframe(dataset, use_container_width=True)

with right:
    st.subheader("Dataset label distribution")
    st.bar_chart(dataset["label"].value_counts())

st.divider()
st.header("Analyze a network traffic record")

col1, col2, col3 = st.columns(3)

with col1:
    duration = st.number_input("Duration", min_value=0, value=1)
    protocol_type = st.selectbox("Protocol", ["tcp", "udp", "icmp"])
    service = st.selectbox("Service", ["http", "https", "dns", "ftp", "private"])
with col2:
    flag = st.selectbox("Connection flag", ["normal", "error"])
    src_bytes = st.number_input("Source bytes", min_value=0, value=500)
    dst_bytes = st.number_input("Destination bytes", min_value=0, value=1000)
with col3:
    count = st.number_input("Connection count", min_value=0, value=5)
    same_srv_rate = st.slider("Same service rate", 0.0, 1.0, 0.8)
    error_rate = st.slider("Error rate", 0.0, 1.0, 0.0)

traffic = {
    "duration": duration,
    "protocol_type": protocol_type,
    "service": service,
    "flag": flag,
    "src_bytes": src_bytes,
    "dst_bytes": dst_bytes,
    "count": count,
    "same_srv_rate": same_srv_rate,
    "error_rate": error_rate,
}

if st.button("Analyze traffic", type="primary"):
    try:
        model = load_model()
        prediction = predict_traffic(model, traffic)[0]

        if prediction == "suspicious":
            st.error("Prediction: Suspicious traffic")
        else:
            st.success("Prediction: Normal traffic")

        st.caption(
            "This is a model prediction, not proof that traffic is safe "
            "or malicious."
        )

    except FileNotFoundError:
        st.error(
            "The trained model is not available yet. Run "
            "`python train_model.py` from the project root first."
        )
    except (ValueError, TypeError, OSError) as exc:
        st.error(f"Prediction failed: {exc}")

st.divider()
st.caption("AI Network Intrusion Detection System | Educational project")
