import streamlit as st

from services.artifacts import load_artifacts, load_metrics
from ui.components import render_header
from ui.performance import render_performance_tab
from ui.screening import render_screening_tab
from ui.sidebar import render_sidebar
from ui.theme import inject_theme

st.set_page_config(
    page_title="Malnutrition Detection System",
    layout="wide",
    page_icon="🩺",
    initial_sidebar_state="expanded",
)

inject_theme()
render_sidebar()
render_header()

log_reg, tree_clf, encoder, features = load_artifacts()
metrics = load_metrics()

screening_tab, performance_tab = st.tabs(["Patient Screening", "Model Performance"])

with screening_tab:
    render_screening_tab(log_reg, tree_clf, encoder, features, metrics)

with performance_tab:
    render_performance_tab(metrics)
