def compute_model_recommendations(metrics: dict) -> dict:
    log_m = metrics["logistic_regression"]
    tree_m = metrics["decision_tree"]

    log_severe_recall = log_m["classification_report"]["severe"]["recall"]
    tree_severe_recall = tree_m["classification_report"]["severe"]["recall"]

    overall_champion = (
        "Decision Tree"
        if tree_m["test_macro_f1"] >= log_m["test_macro_f1"]
        else "Logistic Regression"
    )
    clinical_champion = (
        "Logistic Regression"
        if log_severe_recall >= tree_severe_recall
        else "Decision Tree"
    )

    return {
        "overall_champion": overall_champion,
        "clinical_champion": clinical_champion,
        "log_severe_recall_pct": log_severe_recall * 100,
        "tree_severe_recall_pct": tree_severe_recall * 100,
        "log_macro_f1": log_m["test_macro_f1"],
        "tree_macro_f1": tree_m["test_macro_f1"],
    }
