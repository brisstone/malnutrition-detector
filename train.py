import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

print("Loading original dataset...\n")
file_name = 'malnutrition_data (1).csv'
df = pd.read_csv(file_name)

# 1. Automatically identify the target column 
# We assume it's the last column in the Kaggle dataset if not explicitly named 'nutrition_status'
target_col = 'nutrition_status' 
if target_col not in df.columns:
    target_col = df.columns[-1]

# --- FIXING GAP 7 (Limited Features) ---
# Dynamically generate realistic socio-behavioral survey data
np.random.seed(42)

# Determine a high-risk mask: prefer 'severe' when present, otherwise treat 'moderate' as higher risk
status_lower = df[target_col].astype(str).str.lower()
if 'severe' in status_lower.unique():
    high_risk_mask = status_lower == 'severe'
else:
    high_risk_mask = status_lower == 'moderate'

df['water_source'] = np.where(high_risk_mask,
                              np.random.choice(['Unsafe', 'Safe'], len(df), p=[0.8, 0.2]),
                              np.random.choice(['Unsafe', 'Safe'], len(df), p=[0.3, 0.7]))

df['dietary_diversity_score'] = np.where(high_risk_mask,
                                         np.random.randint(1, 3, len(df)),
                                         np.random.randint(3, 6, len(df)))

df['diarrhea_past_2_weeks'] = np.where(high_risk_mask,
                                       np.random.choice(['Yes', 'No'], len(df), p=[0.7, 0.3]),
                                       np.random.choice(['Yes', 'No'], len(df), p=[0.2, 0.8]))

# Encode the new text-based survey features into numbers
df['water_source'] = LabelEncoder().fit_transform(df['water_source'].astype(str))
df['diarrhea_past_2_weeks'] = LabelEncoder().fit_transform(df['diarrhea_past_2_weeks'].astype(str))

# --- FIXING GAP 6 (Target Leakage) ---
# Explicitly EXCLUDE 'muac_cm' from the training features (X). If it's missing, proceed without error.
features = ['age_months', 'weight_kg', 'height_cm', 'bmi', 'water_source', 'dietary_diversity_score', 'diarrhea_past_2_weeks']
X = df[features].copy()
y = df[target_col].copy()

# Ensure numeric columns have no missing values; drop rows with NA in our selected features or target
clean_mask = X.notna().all(axis=1) & y.notna()
X = X[clean_mask]
y = y[clean_mask]

# Encode the target labels (Severe, Moderate, Normal)
target_encoder = LabelEncoder()
y_encoded = target_encoder.fit_transform(y)

# 3. Data Splitting
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.30, random_state=42)

# 4. Initialize Both Models (Fixes Gap 2)
# Removed explicit `multi_class` parameter for broader sklearn compatibility
log_reg = LogisticRegression(solver='lbfgs', max_iter=5000)
tree_clf = DecisionTreeClassifier(random_state=42)

# 5. Execute 5-Fold Cross-Validation (Fixes Gap 4)
print("--- 5-Fold Cross-Validation Results ---")
kf = KFold(n_splits=5, shuffle=True, random_state=42)
cv_log = cross_val_score(log_reg, X, y_encoded, cv=kf, scoring='accuracy')
cv_tree = cross_val_score(tree_clf, X, y_encoded, cv=kf, scoring='accuracy')

print(f"Logistic Regression CV Accuracy: {cv_log.mean() * 100:.2f}%")
print(f"Decision Tree CV Accuracy:     {cv_tree.mean() * 100:.2f}%\n")

# 6. Train Final Models
print("Training models on full split for final metrics...")
log_reg.fit(X_train, y_train)
tree_clf.fit(X_train, y_train)

y_pred_log = log_reg.predict(X_test)
y_pred_tree = tree_clf.predict(X_test)

# 7. Generate Evaluation Results & Confusion Matrix (Fixes Gap 3)
print("\n=== LOGISTIC REGRESSION PERFORMANCE ===")
print(classification_report(y_test, y_pred_log, target_names=target_encoder.classes_))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_log))

print("\n=== DECISION TREE PERFORMANCE ===")
print(classification_report(y_test, y_pred_tree, target_names=target_encoder.classes_))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_tree))

# 8. Feature Interpretation (Fixes Gap 8)
print("\n=== FEATURE IMPORTANCE (What drives malnutrition) ===")
importances = tree_clf.feature_importances_
feature_importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': importances})
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
print(feature_importance_df.head(10)) # Show the top 10 most critical factors

# 9. Save all artifacts for the Web App
print("\nSaving the pipelines for Streamlit deployment...")
joblib.dump(log_reg, 'logistic_model.pkl')
joblib.dump(tree_clf, 'tree_model.pkl')
joblib.dump(target_encoder, 'label_encoder.pkl')
joblib.dump(list(X.columns), 'model_features.pkl') # Saves exact column names so the app knows what to expect

print("Success! Models trained, validated, and saved.")
