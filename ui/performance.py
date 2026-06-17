import pandas as pd
import streamlit as st

from ui.components import (
    render_classification_table,
    render_confusion_matrix,
    render_metric_tile,
    section_card,
)


def render_performance_tab(metrics: dict | None) -> None:
    st.markdown("### Model Performance")
    st.caption("Evaluation summary from the held-out test set and 5-fold cross-validation.")

    if metrics is None:
        st.warning("No `models/metrics.json` found. Run `python train.py` to generate evaluation results.")
        return

    classes = metrics["classes"]
    log_m = metrics["logistic_regression"]
    tree_m = metrics["decision_tree"]

    tile_cols = st.columns(4, gap="medium")
    tiles = [
        ("LR CV Accuracy", f"{log_m['cv_accuracy_mean'] * 100:.1f}%"),
        ("LR Test Accuracy", f"{log_m['test_accuracy'] * 100:.1f}%"),
        ("DT CV Accuracy", f"{tree_m['cv_accuracy_mean'] * 100:.1f}%"),
        ("DT Test Accuracy", f"{tree_m['test_accuracy'] * 100:.1f}%"),
    ]
    for col, (label, value) in zip(tile_cols, tiles):
        with col:
            render_metric_tile(label, value)

    st.markdown("")
    summary = pd.DataFrame(
        [
            {
                "Model": "Logistic Regression",
                "CV Accuracy": f"{log_m['cv_accuracy_mean'] * 100:.2f}% ± {log_m['cv_accuracy_std'] * 100:.2f}%",
                "Test Accuracy": f"{log_m['test_accuracy'] * 100:.2f}%",
                "Test Macro F1": f"{log_m['test_macro_f1']:.3f}",
            },
            {
                "Model": "Decision Tree",
                "CV Accuracy": f"{tree_m['cv_accuracy_mean'] * 100:.2f}% ± {tree_m['cv_accuracy_std'] * 100:.2f}%",
                "Test Accuracy": f"{tree_m['test_accuracy'] * 100:.2f}%",
                "Test Macro F1": f"{tree_m['test_macro_f1']:.3f}",
            },
        ]
    )
    st.dataframe(summary, use_container_width=True, hide_index=True)

    perf_col1, perf_col2 = st.columns(2, gap="medium")

    with perf_col1:
        with section_card("Logistic Regression", "Per-class metrics and confusion matrix."):
            st.dataframe(
                render_classification_table(log_m["classification_report"], classes),
                use_container_width=True,
                hide_index=True,
            )
            st.markdown("**Confusion matrix**")
            st.dataframe(
                render_confusion_matrix(log_m["confusion_matrix"], classes),
                use_container_width=True,
            )

    with perf_col2:
        with section_card("Decision Tree", "Per-class metrics and confusion matrix."):
            st.dataframe(
                render_classification_table(tree_m["classification_report"], classes),
                use_container_width=True,
                hide_index=True,
            )
            st.markdown("**Confusion matrix**")
            st.dataframe(
                render_confusion_matrix(tree_m["confusion_matrix"], classes),
                use_container_width=True,
            )

    st.markdown("#### Feature Importance (Decision Tree)")
    importance_df = pd.DataFrame(
        list(tree_m["feature_importance"].items()),
        columns=["Feature", "Importance"],
    ).sort_values("Importance", ascending=False)
    st.bar_chart(importance_df.set_index("Feature"))

    st.markdown("#### Logistic Regression Coefficients")
    coef_df = pd.DataFrame(
        list(log_m["coefficients"].items()),
        columns=["Feature", "Coefficient"],
    ).sort_values("Coefficient", key=abs, ascending=False)
    st.dataframe(coef_df, use_container_width=True, hide_index=True)

    with st.expander("Methodology notes"):
        for key, value in metrics["methodology"].items():
            st.write(f"**{key.replace('_', ' ').title()}:** {value}")
