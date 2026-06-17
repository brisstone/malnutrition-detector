from datetime import datetime, timezone

import pandas as pd


def build_screening_report(result: dict) -> dict:
    """Return CSV string and plain-text summary for download."""
    timestamp = result.get("timestamp", datetime.now(timezone.utc).isoformat())
    agreement = "Yes" if result["agreement"] else "No"

    row = {
        "timestamp_utc": timestamp,
        "age_months": result["age"],
        "weight_kg": result["weight"],
        "height_cm": result["height"],
        "bmi": round(result["bmi"], 2),
        "water_source": result["water"],
        "diarrhea_past_2_weeks": result["diarrhea"],
        "dietary_diversity_score": result["diet_score"],
        "logistic_regression_prediction": result["pred_log"],
        "logistic_regression_confidence": round(result["conf_log"] * 100, 1),
        "decision_tree_prediction": result["pred_tree"],
        "decision_tree_confidence": round(result["conf_tree"] * 100, 1),
        "models_agree": agreement,
    }

    csv_data = pd.DataFrame([row]).to_csv(index=False)

    text_summary = f"""Malnutrition Screening Report
Generated: {timestamp}

PATIENT INPUTS
--------------
Age (months):              {result['age']}
Weight (kg):               {result['weight']}
Height (cm):               {result['height']}
BMI:                       {result['bmi']:.2f}
Water source:              {result['water']}
Diarrhea (past 2 weeks):   {result['diarrhea']}
Dietary diversity (1-6):   {result['diet_score']}

MODEL OUTPUTS
-------------
Logistic Regression:       {result['pred_log'].upper()} ({result['conf_log'] * 100:.1f}% confidence)
Decision Tree:             {result['pred_tree'].upper()} ({result['conf_tree'] * 100:.1f}% confidence)
Models agree:              {agreement}

DISCLAIMER
----------
Clinical decision-support only. Confirm with local protocols and physical examination.
"""

    return {"csv": csv_data, "text": text_summary}
