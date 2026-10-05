from src.models.predict import predict_churn


CUSTOMER = {
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 5,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "No",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "Yes",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 95.50,
    "TotalCharges": 477.50
}


def test_prediction_output():

    result = predict_churn(CUSTOMER)

    assert 0 <= result["churn_probability"] <= 1

    assert result["risk_level"] in {
        "Low",
        "Medium",
        "High"
    }

    assert result["prediction"] in {0, 1}

    assert result["monthly_revenue_at_risk"] >= 0