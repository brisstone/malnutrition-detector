from datetime import datetime, timezone

import pandas as pd
import streamlit as st

from ui.components import (
    render_agreement_banner,
    render_bmi_card,
    render_out_of_range_warning,
    render_prediction_card,
    section_card,
)
from ui.constants import TRAINING_RANGES
from ui.recommendations import compute_model_recommendations
from ui.reports import build_screening_report


def _check_input_ranges(age: float, weight: float, height: float) -> list[str]:
    warnings = []
    age_min, age_max = TRAINING_RANGES["age_months"]
    weight_min, weight_max = TRAINING_RANGES["weight_kg"]
    height_min, height_max = TRAINING_RANGES["height_cm"]

    if age < age_min or age > age_max:
        warnings.append(f"Age {age:.0f} months is outside the training range ({age_min}–{age_max}).")
    if weight < weight_min or weight > weight_max:
        warnings.append(f"Weight {weight:.1f} kg is outside the training range ({weight_min}–{weight_max}).")
    if height < height_min or height > height_max:
        warnings.append(f"Height {height:.1f} cm is outside the training range ({height_min}–{height_max}).")
    return warnings


def _predict_with_confidence(model, encoder, input_data: pd.DataFrame) -> tuple[str, float]:
    encoded = model.predict(input_data)[0]
    label = encoder.inverse_transform([encoded])[0]
    probabilities = model.predict_proba(input_data)[0]
    confidence = float(max(probabilities))
    return label, confidence


def _render_results(result: dict, metrics) -> None:
    st.markdown("---")
    st.markdown("### Diagnostic Comparison")

    log_accuracy = metrics["logistic_regression"]["test_accuracy"] if metrics else None
    tree_accuracy = metrics["decision_tree"]["test_accuracy"] if metrics else None

    log_badge = None
    tree_badge = None
    if metrics:
        rec = compute_model_recommendations(metrics)
        if rec["clinical_champion"] == "Logistic Regression":
            log_badge = "Recommended for screening"
        if rec["overall_champion"] == "Decision Tree":
            tree_badge = "Overall metrics champion"

    res_col1, res_col2 = st.columns(2, gap="medium")
    with res_col1:
        render_prediction_card(
            "Multinomial Logistic Regression",
            result["pred_log"],
            result["conf_log"],
            log_accuracy,
            badge=log_badge,
        )
    with res_col2:
        render_prediction_card(
            "Decision Tree Classifier",
            result["pred_tree"],
            result["conf_tree"],
            tree_accuracy,
            badge=tree_badge,
        )

    render_agreement_banner(result["agreement"])

    report = build_screening_report(result)
    dl_col1, dl_col2 = st.columns(2, gap="medium")
    with dl_col1:
        st.download_button(
            label="Download CSV Report",
            data=report["csv"],
            file_name="malnutrition_screening_report.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with dl_col2:
        st.download_button(
            label="Download Text Summary",
            data=report["text"],
            file_name="malnutrition_screening_report.txt",
            mime="text/plain",
            use_container_width=True,
        )


def render_screening_tab(log_reg, tree_clf, encoder, features, metrics) -> None:
    st.markdown("### Patient Screening")
    st.caption("Enter patient vitals and household indicators, then compare model outputs.")

    col1, col2, col3 = st.columns([1.1, 1.1, 0.9], gap="medium")

    with col1:
        with section_card("Anthropometric Data", "Core growth measurements for children 6–59 months."):
            age = st.number_input("Age (months)", min_value=6, max_value=59, value=24, step=1)
            weight = st.number_input("Weight (kg)", min_value=2.0, max_value=30.0, value=10.0, step=0.1)
            height = st.number_input("Height (cm)", min_value=40.0, max_value=130.0, value=80.0, step=0.1)

    with col2:
        with section_card("Socio-Behavioural Data", "Household and recent health context."):
            water = st.selectbox("Primary Water Source", ["Safe", "Unsafe"])
            diarrhea = st.selectbox("Diarrhea in Past 2 Weeks?", ["No", "Yes"])
            diet_score = st.slider("Dietary Diversity Score (1–6)", min_value=1, max_value=6, value=3)

    with col3:
        with section_card("Auto-Calculated Metrics", "Derived at screening time from entered vitals."):
            height_m = height / 100
            bmi = weight / (height_m**2)
            render_bmi_card(bmi)

    render_out_of_range_warning(_check_input_ranges(age, weight, height))

    if st.button("Generate Diagnostic Comparison", use_container_width=True, type="primary"):
        water_encoded = 0 if water == "Safe" else 1
        diarrhea_encoded = 0 if diarrhea == "No" else 1

        input_data = pd.DataFrame(
            [[age, weight, height, bmi, water_encoded, diet_score, diarrhea_encoded]],
            columns=features,
        )

        with st.spinner("Running logistic regression and decision tree models..."):
            pred_log, conf_log = _predict_with_confidence(log_reg, encoder, input_data)
            pred_tree, conf_tree = _predict_with_confidence(tree_clf, encoder, input_data)

        st.session_state["screening_result"] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "age": age,
            "weight": weight,
            "height": height,
            "bmi": bmi,
            "water": water,
            "diarrhea": diarrhea,
            "diet_score": diet_score,
            "pred_log": pred_log,
            "conf_log": conf_log,
            "pred_tree": pred_tree,
            "conf_tree": conf_tree,
            "agreement": pred_log == pred_tree,
        }

    if "screening_result" in st.session_state:
        _render_results(st.session_state["screening_result"], metrics)
