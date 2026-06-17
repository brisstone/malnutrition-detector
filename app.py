import streamlit as st
import pandas as pd
import joblib

# 1. Page Configuration and Custom Styling
st.set_page_config(page_title="Malnutrition Detection System", layout="wide", page_icon="🩺")

st.markdown("""
<style>
.stButton>button {
    background-color: #8B4513;
    color: white;
    border: none;
    border-radius: 5px;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #A0522D;
    color: white;
}
h1, h2, h3 {
    color: #5C3317;
}
.metric-card {
    background-color: #fdf5e6;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #8B4513;
}
</style>
""", unsafe_allow_html=True)

# 2. Load the trained models and artifacts
@st.cache_resource
def load_artifacts():
    try:
        log_reg = joblib.load('logistic_model.pkl')
        tree_clf = joblib.load('tree_model.pkl')
        encoder = joblib.load('label_encoder.pkl')
        features = joblib.load('model_features.pkl')
        return log_reg, tree_clf, encoder, features
    except Exception as e:
        st.error(f"Error loading models: {e}")
        st.stop()

log_reg, tree_clf, encoder, features = load_artifacts()

st.title("🩺 Advanced Malnutrition Detection System")
st.write("Evaluate pediatric nutritional risk using combined anthropometric and socio-behavioral clinical indicators.")
st.markdown("---")

# 3. Input Form for Health Workers
st.subheader("Patient Diagnostics Form")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Anthropometric Data**")
    age = st.number_input("Age (in months)", min_value=6, max_value=59, value=24)
    weight = st.number_input("Weight (kg)", min_value=2.0, max_value=30.0, value=10.0, step=0.1)
    height = st.number_input("Height (cm)", min_value=40.0, max_value=130.0, value=80.0, step=0.1)

with col2:
    st.markdown("**Socio-Behavioral Data**")
    water = st.selectbox("Primary Water Source", ["Safe", "Unsafe"])
    diarrhea = st.selectbox("Diarrhea in Past 2 Weeks?", ["No", "Yes"])
    diet_score = st.slider("Dietary Diversity Score (1-6)", min_value=1, max_value=6, value=3)

with col3:
    st.markdown("**Auto-Calculated Metrics**")
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    st.markdown(f"<div class='metric-card'><h3>Patient BMI</h3><h2>{bmi:.2f}</h2></div>", unsafe_allow_html=True)

# 4. Data Processing & Prediction
if st.button("Generate Diagnostic Comparison", use_container_width=True):
    water_encoded = 0 if water == "Safe" else 1
    diarrhea_encoded = 0 if diarrhea == "No" else 1

    input_data = pd.DataFrame(
        [[age, weight, height, bmi, water_encoded, diet_score, diarrhea_encoded]],
        columns=features,
    )

    pred_log = encoder.inverse_transform(log_reg.predict(input_data))[0]
    pred_tree = encoder.inverse_transform(tree_clf.predict(input_data))[0]

    st.markdown("---")
    st.subheader("Model Comparison & Results")

    res_col1, res_col2 = st.columns(2)

    with res_col1:
        st.markdown("#### Multinomial Logistic Regression")
        st.caption("Primary Clinical Model (Accuracy: 91.64%)")
        if pred_log == 'severe':
            st.error("🚨 SEVERE MALNUTRITION")
        elif pred_log == 'moderate':
            st.warning("⚠️ MODERATE MALNUTRITION")
        else:
            st.success("✅ NORMAL")

    with res_col2:
        st.markdown("#### Decision Tree Classifier")
        st.caption("Secondary Verification Model (Accuracy: 89.92%)")
        if pred_tree == 'severe':
            st.error("🚨 SEVERE MALNUTRITION")
        elif pred_tree == 'moderate':
            st.warning("⚠️ MODERATE MALNUTRITION")
        else:
            st.success("✅ NORMAL")
