import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "malnutrition_data.csv"
MODELS_DIR = ROOT / "models"
MODELS_DIR.mkdir(exist_ok=True)

print("Loading original dataset...\n")
df = pd.read_csv(DATA_PATH)

target_col = "nutrition_status"
if target_col not in df.columns:
    target_col = df.columns[-1]

# Recompute BMI from weight and height (ignore inconsistent CSV values)
df["bmi"] = df["weight_kg"] / (df["height_cm"] / 100) ** 2

# Simulate socio-behavioural survey data from anthropometric risk — NOT from labels
np.random.seed(42)
bmi_threshold = df["bmi"].quantile(0.25)
weight_threshold = df["weight_kg"].quantile(0.25)
anthro_risk_mask = (df["bmi"] < bmi_threshold) | (df["weight_kg"] < weight_threshold)

n = len(df)
df["water_source"] = np.where(
    anthro_risk_mask,
    np.random.choice(["Unsafe", "Safe"], n, p=[0.6, 0.4]),
    np.random.choice(["Unsafe", "Safe"], n, p=[0.25, 0.75]),
)
df["dietary_diversity_score"] = np.where(
    anthro_risk_mask,
    np.random.randint(1, 4, n),
    np.random.randint(3, 7, n),
)
df["diarrhea_past_2_weeks"] = np.where(
    anthro_risk_mask,
    np.random.choice(["Yes", "No"], n, p=[0.55, 0.45]),
    np.random.choice(["Yes", "No"], n, p=[0.2, 0.8]),
)

# Explicit encoding — must match app.py
df["water_source"] = df["water_source"].map({"Safe": 0, "Unsafe": 1})
df["diarrhea_past_2_weeks"] = df["diarrhea_past_2_weeks"].map({"No": 0, "Yes": 1})

# Exclude MUAC to avoid single-variable rule memorisation
features = [
    "age_months",
    "weight_kg",
    "height_cm",
    "bmi",
    "water_source",
    "dietary_diversity_score",
    "diarrhea_past_2_weeks",
]
X = df[features].copy()
y = df[target_col].copy()

clean_mask = X.notna().all(axis=1) & y.notna()
X = X[clean_mask]
y = y[clean_mask]

target_encoder = LabelEncoder()
y_encoded = target_encoder.fit_transform(y)
class_names = list(target_encoder.classes_)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.30,
    random_state=42,
    stratify=y_encoded,
)

log_reg = LogisticRegression(solver="lbfgs", max_iter=5000, class_weight="balanced")
tree_clf = DecisionTreeClassifier(random_state=42, class_weight="balanced")

print("--- 5-Fold Stratified Cross-Validation (training set only) ---")
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_log = cross_val_score(log_reg, X_train, y_train, cv=cv, scoring="accuracy")
cv_tree = cross_val_score(tree_clf, X_train, y_train, cv=cv, scoring="accuracy")
print(f"Logistic Regression CV Accuracy: {cv_log.mean() * 100:.2f}% (+/- {cv_log.std() * 100:.2f}%)")
print(f"Decision Tree CV Accuracy:     {cv_tree.mean() * 100:.2f}% (+/- {cv_tree.std() * 100:.2f}%)\n")

print("Training models on stratified split...")
log_reg.fit(X_train, y_train)
tree_clf.fit(X_train, y_train)

y_pred_log = log_reg.predict(X_test)
y_pred_tree = tree_clf.predict(X_test)

log_report = classification_report(
    y_test, y_pred_log, target_names=class_names, output_dict=True
)
tree_report = classification_report(
    y_test, y_pred_tree, target_names=class_names, output_dict=True
)
log_cm = confusion_matrix(y_test, y_pred_log).tolist()
tree_cm = confusion_matrix(y_test, y_pred_tree).tolist()

print("\n=== LOGISTIC REGRESSION (test set) ===")
print(classification_report(y_test, y_pred_log, target_names=class_names))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_log))

print("\n=== DECISION TREE (test set) ===")
print(classification_report(y_test, y_pred_tree, target_names=class_names))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_tree))

feature_importance = dict(
    zip(features, tree_clf.feature_importances_.tolist())
)
lr_coefficients = dict(
    zip(features, log_reg.coef_.mean(axis=0).tolist())
)
sorted_importance = dict(
    sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
)

print("\n=== FEATURE IMPORTANCE (Decision Tree) ===")
for name, score in sorted_importance.items():
    print(f"  {name}: {score:.4f}")

metrics = {
    "classes": class_names,
    "methodology": {
        "bmi": "Recomputed from weight_kg and height_cm",
        "muac_excluded": True,
        "socio_behavioural_source": "Simulated from anthropometric risk quartiles (not from nutrition labels)",
        "train_test_split": "70/30 stratified",
        "class_weight": "balanced",
        "cross_validation": "5-fold stratified on training set",
    },
    "logistic_regression": {
        "cv_accuracy_mean": float(cv_log.mean()),
        "cv_accuracy_std": float(cv_log.std()),
        "test_accuracy": float(accuracy_score(y_test, y_pred_log)),
        "test_macro_f1": float(f1_score(y_test, y_pred_log, average="macro")),
        "classification_report": log_report,
        "confusion_matrix": log_cm,
        "coefficients": lr_coefficients,
    },
    "decision_tree": {
        "cv_accuracy_mean": float(cv_tree.mean()),
        "cv_accuracy_std": float(cv_tree.std()),
        "test_accuracy": float(accuracy_score(y_test, y_pred_tree)),
        "test_macro_f1": float(f1_score(y_test, y_pred_tree, average="macro")),
        "classification_report": tree_report,
        "confusion_matrix": tree_cm,
        "feature_importance": sorted_importance,
    },
}

print("\nSaving artifacts...")
joblib.dump(log_reg, MODELS_DIR / "logistic_regression.pkl")
joblib.dump(tree_clf, MODELS_DIR / "decision_tree.pkl")
joblib.dump(target_encoder, MODELS_DIR / "label_encoder.pkl")
joblib.dump(features, MODELS_DIR / "feature_names.pkl")

with (MODELS_DIR / "metrics.json").open("w") as f:
    json.dump(metrics, f, indent=2)

print("Success! Models and metrics saved to models/")
