import json
from pathlib import Path

import joblib
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = ROOT / "models"


@st.cache_resource
def load_artifacts():
    try:
        log_reg = joblib.load(MODELS_DIR / "logistic_regression.pkl")
        tree_clf = joblib.load(MODELS_DIR / "decision_tree.pkl")
        encoder = joblib.load(MODELS_DIR / "label_encoder.pkl")
        features = joblib.load(MODELS_DIR / "feature_names.pkl")
        return log_reg, tree_clf, encoder, features
    except Exception as e:
        st.error(f"Error loading models: {e}")
        st.stop()


@st.cache_data
def load_metrics():
    metrics_path = MODELS_DIR / "metrics.json"
    if not metrics_path.exists():
        return None
    with metrics_path.open() as f:
        return json.load(f)
