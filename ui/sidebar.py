import streamlit as st


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("### Screening Guide")
        st.caption("Reference values for frontline health workers.")

        st.markdown("**WHO MUAC cutoffs (6–59 months)**")
        st.markdown(
            """
| Status | MUAC |
|--------|------|
| **Severe** | < 11.5 cm |
| **Moderate** | 11.5 – 12.5 cm |
| **Normal** | ≥ 12.5 cm |
            """
        )

        st.divider()
        st.markdown("**Screening tips**")
        st.markdown(
            """
- Measure MUAC on the **left arm**, mid-point between shoulder and elbow.
- Record weight and height **before** running the model.
- Ask about **recent diarrhea** and **diet variety** in the past week.
- Treat **severe** cases as urgent referral candidates.
- When models **disagree**, use clinical judgement ; do not rely on the app alone.
            """
        )

        st.divider()
        st.markdown("**About this tool**")
        st.caption(
            "Combines anthropometric vitals with socio-behavioural indicators. "
            "Outputs are decision-support classifications, not a clinical diagnosis."
        )
