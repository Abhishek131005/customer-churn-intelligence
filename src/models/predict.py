from pathlib import Path

import joblib
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "churn_pipeline.joblib"
)


# Load trained pipeline
model = joblib.load(MODEL_PATH)


def get_risk_level(probability):
    if probability >= 0.70:
        return "High"

    if probability >= 0.40:
        return "Medium"

    return "Low"


def predict_churn(customer_data, threshold=0.40):
    customer_df = pd.DataFrame([customer_data])

    probability = float(
        model.predict_proba(customer_df)[0, 1]
    )

    prediction = int(probability >= threshold)

    monthly_charges = float(
        customer_data["MonthlyCharges"]
    )

    revenue_at_risk = (
        probability * monthly_charges
    )

    return {
        "prediction": prediction,
        "prediction_label": (
            "Likely to Churn"
            if prediction == 1
            else "Likely to Stay"
        ),
        "churn_probability": round(probability, 4),
        "risk_level": get_risk_level(probability),
        "monthly_revenue_at_risk": round(revenue_at_risk, 2)
    }