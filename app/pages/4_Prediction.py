import streamlit as st

from app.services.api_client import (
    predict_customer,
    check_api_health
)

from app.components.styles import load_css, page_header


load_css()


page_header(
    "Customer Risk Assessment",
    "Evaluate an individual customer's churn probability and financial exposure."
)
if check_api_health():
    st.caption("● Prediction service online")
else:
    st.warning(
        "Prediction API is offline. "
        "Start the FastAPI service before making predictions."
    )
st.markdown("### Customer Profile")

c1, c2, c3, c4 = st.columns(4)

with c1:
    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

with c2:
    senior = st.selectbox(
        "Senior Citizen",
        [0, 1]
    )

with c3:
    partner = st.selectbox(
        "Partner",
        ["Yes", "No"]
    )

with c4:
    dependents = st.selectbox(
        "Dependents",
        ["Yes", "No"]
    )

st.markdown("### Account")

c1, c2, c3 = st.columns(3)

with c1:
    tenure = st.number_input(
        "Tenure (months)",
        0,
        72,
        12
    )

with c2:
    contract = st.selectbox(
        "Contract",
        [
            "Month-to-month",
            "One year",
            "Two year"
        ]
    )

with c3:
    payment = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )

st.markdown("### Services")

c1, c2, c3 = st.columns(3)

with c1:
    phone = st.selectbox(
        "Phone Service",
        ["Yes", "No"]
    )

    multiple = st.selectbox(
        "Multiple Lines",
        ["No", "Yes", "No phone service"]
    )

    internet = st.selectbox(
        "Internet Service",
        ["DSL", "Fiber optic", "No"]
    )

with c2:
    security = st.selectbox(
        "Online Security",
        ["No", "Yes", "No internet service"]
    )

    backup = st.selectbox(
        "Online Backup",
        ["No", "Yes", "No internet service"]
    )

    protection = st.selectbox(
        "Device Protection",
        ["No", "Yes", "No internet service"]
    )

with c3:
    support = st.selectbox(
        "Tech Support",
        ["No", "Yes", "No internet service"]
    )

    tv = st.selectbox(
        "Streaming TV",
        ["No", "Yes", "No internet service"]
    )

    movies = st.selectbox(
        "Streaming Movies",
        ["No", "Yes", "No internet service"]
    )
st.markdown("### Billing")

c1, c2, c3 = st.columns(3)

with c1:
    paperless = st.selectbox(
        "Paperless Billing",
        ["Yes", "No"]
    )

with c2:
    monthly = st.number_input(
        "Monthly Charges ($)",
        min_value=0.0,
        value=70.0
    )

with c3:
    total = st.number_input(
        "Total Charges ($)",
        min_value=0.0,
        value=840.0
    )
    
customer = {
    "gender": gender,
    "SeniorCitizen": senior,
    "Partner": partner,
    "Dependents": dependents,
    "tenure": tenure,
    "PhoneService": phone,
    "MultipleLines": multiple,
    "InternetService": internet,
    "OnlineSecurity": security,
    "OnlineBackup": backup,
    "DeviceProtection": protection,
    "TechSupport": support,
    "StreamingTV": tv,
    "StreamingMovies": movies,
    "Contract": contract,
    "PaperlessBilling": paperless,
    "PaymentMethod": payment,
    "MonthlyCharges": monthly,
    "TotalCharges": total
}


st.markdown("")

if st.button(
    "Analyze Customer",
    type="primary",
    use_container_width=True
):

    try:
        result = predict_customer(customer)

    except Exception:
        st.error(
            "Prediction service is currently unavailable. "
            "Please try again shortly."
        )
        st.stop()   

    probability = (
        result["churn_probability"] * 100
    )

    risk = result["risk_level"]

    st.markdown("---")

    st.markdown("## Risk Assessment")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Churn Probability",
        f"{probability:.1f}%"
    )

    c2.metric(
        "Risk Level",
        risk
    )

    c3.metric(
        "Monthly Revenue at Risk",
        f"${result['monthly_revenue_at_risk']:.2f}"
    )

    st.progress(
        result["churn_probability"]
    )

    if risk == "High":

        st.markdown(
            """
            <div class="risk-high">
            <strong>High retention priority</strong><br>
            This customer has a high predicted likelihood of churn
            and should be considered for proactive retention action.
            </div>
            """,
            unsafe_allow_html=True
        )

    elif risk == "Medium":

        st.markdown(
            """
            <div class="risk-medium">
            <strong>Moderate retention priority</strong><br>
            Monitor this customer and consider targeted engagement.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="risk-low">
            <strong>Low retention priority</strong><br>
            Current churn probability is relatively low.
            </div>
            """,
            unsafe_allow_html=True
        )