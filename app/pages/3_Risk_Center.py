from pathlib import Path

import pandas as pd
import streamlit as st

from src.models.predict import model, get_risk_level
from app.components.styles import load_css, page_header


load_css()

PROJECT_ROOT = Path(__file__).resolve().parents[2]

df = pd.read_csv(
    PROJECT_ROOT
    / "data"
    / "processed"
    / "telco_churn_clean.csv"
)


page_header(
    "Customer Risk Center",
    "Prioritize customers using predicted churn probability and revenue exposure."
)


X = df.drop(
    columns=["Churn", "customerID"]
)


probabilities = model.predict_proba(X)[:, 1]


risk_df = pd.DataFrame({
    "Customer ID": df["customerID"],
    "Churn Probability": probabilities,
    "Risk Level": [
        get_risk_level(p)
        for p in probabilities
    ],
    "Monthly Revenue": df["MonthlyCharges"]
})


risk_df["Revenue at Risk"] = (
    risk_df["Churn Probability"]
    * risk_df["Monthly Revenue"]
)


risk_df["Churn Probability"] = (
    risk_df["Churn Probability"] * 100
)


# --------------------------------
# KPIs
# --------------------------------

high_risk = (
    risk_df["Risk Level"] == "High"
).sum()

total_revenue_risk = (
    risk_df["Revenue at Risk"]
).sum()


c1, c2, c3 = st.columns(3)

c1.metric(
    "High-Risk Customers",
    f"{high_risk:,}"
)

c2.metric(
    "Expected Monthly Revenue Risk",
    f"${total_revenue_risk:,.0f}"
)

c3.metric(
    "Average Churn Probability",
    f"{risk_df['Churn Probability'].mean():.1f}%"
)


st.markdown("## Retention Priority Queue")


risk_filter = st.multiselect(
    "Risk level",
    ["High", "Medium", "Low"],
    default=["High"]
)


filtered = risk_df[
    risk_df["Risk Level"].isin(
        risk_filter
    )
]


filtered = filtered.sort_values(
    "Revenue at Risk",
    ascending=False
)


st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Churn Probability":
            st.column_config.ProgressColumn(
                "Churn Probability",
                min_value=0,
                max_value=100,
                format="%.1f%%"
            ),

        "Monthly Revenue":
            st.column_config.NumberColumn(
                format="$%.2f"
            ),

        "Revenue at Risk":
            st.column_config.NumberColumn(
                format="$%.2f"
            )
    }
)