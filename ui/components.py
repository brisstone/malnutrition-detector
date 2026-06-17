import html
from contextlib import contextmanager

import pandas as pd
import streamlit as st

STATUS_CONFIG = {
    "severe": {
        "badge_class": "badge-severe",
        "card_class": "severe",
        "fill_class": "fill-severe",
        "label": "Severe Malnutrition",
        "message": "Immediate clinical intervention and referral are recommended.",
    },
    "moderate": {
        "badge_class": "badge-moderate",
        "card_class": "moderate",
        "fill_class": "fill-moderate",
        "label": "Moderate Malnutrition",
        "message": "Nutritional support and close follow-up monitoring are advised.",
    },
    "normal": {
        "badge_class": "badge-normal",
        "card_class": "normal",
        "fill_class": "fill-normal",
        "label": "Normal Nutritional Status",
        "message": "No acute malnutrition indicators detected by the model.",
    },
}


def render_header() -> None:
    st.markdown(
        """
        <div class="hero">
            <h1>Advanced Malnutrition Detection System</h1>
            <p>Evaluate pediatric nutritional risk using anthropometric vitals and
            socio-behavioural indicators for frontline health screening.</p>
        </div>
        <div class="disclaimer">
            Clinical decision-support only. Confirm all results with local protocols,
            physical examination, and MUAC screening where available.
        </div>
        """,
        unsafe_allow_html=True,
    )


@contextmanager
def section_card(title: str, hint: str = ""):
    with st.container(border=True):
        st.markdown(f"**{title}**")
        if hint:
            st.caption(hint)
        yield


def render_bmi_card(bmi: float) -> None:
    category = "Underweight range" if bmi < 14 else "Within typical screening range"
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Patient BMI</div>
            <div class="kpi-value">{bmi:.2f}</div>
            <div class="kpi-sub">{category}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_tile(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="metric-tile">
            <div class="label">{html.escape(label)}</div>
            <div class="value">{html.escape(value)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_model_recommendations(metrics: dict) -> None:
    from ui.recommendations import compute_model_recommendations

    rec = compute_model_recommendations(metrics)
    st.markdown(
        f"""
        <div class="recommendation-panel">
            <div class="recommendation-card champion-overall">
                <div class="recommendation-label">Overall metrics champion</div>
                <div class="recommendation-model">{html.escape(rec["overall_champion"])}</div>
                <div class="recommendation-detail">
                    Highest test macro F1
                    (LR {rec["log_macro_f1"]:.3f} vs DT {rec["tree_macro_f1"]:.3f})
                </div>
            </div>
            <div class="recommendation-card champion-clinical">
                <div class="recommendation-label">Recommended for screening</div>
                <div class="recommendation-model">{html.escape(rec["clinical_champion"])}</div>
                <div class="recommendation-detail">
                    Best severe-class recall
                    (LR {rec["log_severe_recall_pct"]:.1f}% vs DT {rec["tree_severe_recall_pct"]:.1f}%)
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_prediction_card(
    model_name: str,
    label: str,
    confidence: float,
    test_accuracy: float | None = None,
    badge: str | None = None,
) -> None:
    config = STATUS_CONFIG.get(label, STATUS_CONFIG["normal"])
    accuracy_text = (
        f"Test accuracy: {test_accuracy * 100:.1f}%" if test_accuracy is not None else ""
    )
    badge_html = (
        f'<div class="model-badge">{html.escape(badge)}</div>' if badge else ""
    )
    st.markdown(
        f"""
        <div class="result-card {config['card_class']}">
            {badge_html}
            <div class="result-title">{html.escape(model_name)}</div>
            <div class="result-badge {config['badge_class']}">{config['label']}</div>
            <div class="result-message">{config['message']}</div>
            <div class="confidence-label">Prediction confidence: {confidence * 100:.1f}%</div>
            <div class="confidence-track">
                <div class="confidence-fill {config['fill_class']}"
                     style="width: {min(confidence * 100, 100):.1f}%"></div>
            </div>
            <div class="kpi-sub" style="margin-top:0.55rem;">{accuracy_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_agreement_banner(agrees: bool) -> None:
    if agrees:
        st.markdown(
            """
            <div class="agreement match">
                <strong>Model agreement:</strong> Both models reached the same classification
                for this patient.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="agreement mismatch">
                <strong>Model disagreement:</strong> Models produced different results.
                Use clinical judgement and local referral protocols before acting.
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_out_of_range_warning(messages: list[str]) -> None:
    if not messages:
        return
    joined = " ".join(messages)
    st.markdown(
        f'<div class="warning-chip"><strong>Input notice:</strong> {html.escape(joined)}</div>',
        unsafe_allow_html=True,
    )


def render_classification_table(report: dict, classes: list[str]) -> pd.DataFrame:
    rows = []
    for label in classes:
        rows.append(
            {
                "Class": label,
                "Precision": report[label]["precision"],
                "Recall": report[label]["recall"],
                "F1-Score": report[label]["f1-score"],
                "Support": int(report[label]["support"]),
            }
        )
    rows.append(
        {
            "Class": "macro avg",
            "Precision": report["macro avg"]["precision"],
            "Recall": report["macro avg"]["recall"],
            "F1-Score": report["macro avg"]["f1-score"],
            "Support": int(report["macro avg"]["support"]),
        }
    )
    return pd.DataFrame(rows)
