from pathlib import Path

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from sklearn.linear_model import LogisticRegression

from src.data.preprocess import build_preprocessor


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "telco_churn_clean.csv"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "churn_pipeline.joblib"
)


# --------------------------------------------------
# Load data
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

print(f"Loaded dataset: {df.shape}")


# --------------------------------------------------
# Prepare features and target
# --------------------------------------------------

X = df.drop(
    columns=["Churn", "customerID"]
)

y = df["Churn"].map({
    "No": 0,
    "Yes": 1
})


# --------------------------------------------------
# Train-test split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# --------------------------------------------------
# Preprocessing
# --------------------------------------------------

preprocessor = build_preprocessor(X_train)


# --------------------------------------------------
# Model
# --------------------------------------------------

classifier = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)


# --------------------------------------------------
# Complete pipeline
# --------------------------------------------------

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", classifier)
])


# --------------------------------------------------
# Train
# --------------------------------------------------

print("Training model...")

pipeline.fit(X_train, y_train)


# --------------------------------------------------
# Evaluate
# --------------------------------------------------

predictions = pipeline.predict(X_test)
probabilities = pipeline.predict_proba(X_test)[:, 1]

print("\nModel Performance")
print("-----------------")

print(
    f"Accuracy:  {accuracy_score(y_test, predictions):.3f}"
)

print(
    f"Precision: {precision_score(y_test, predictions):.3f}"
)

print(
    f"Recall:    {recall_score(y_test, predictions):.3f}"
)

print(
    f"F1 Score:  {f1_score(y_test, predictions):.3f}"
)

print(
    f"ROC-AUC:   {roc_auc_score(y_test, probabilities):.3f}"
)


# --------------------------------------------------
# Save pipeline
# --------------------------------------------------

MODEL_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(
    pipeline,
    MODEL_PATH
)

print(
    f"\nModel saved to: {MODEL_PATH}"
)