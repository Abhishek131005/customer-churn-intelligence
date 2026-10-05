from pathlib import Path
import sys

import pandas as pd
import streamlit as st

# --------------------------------------------------
# Make project root importable
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.models.predict import model, get_risk_level
from app.components.styles import load_css, page_header


# --------------------------------------------------
# Page setup
# --------------------------------------------------

load_css()

page_header(
    "Customer Risk Center",
    "Prioritize customers using predicted churn probability and revenue exposure."
)


# --------------------------------------------------
# Load cleaned customer data
# --------------------------------------------------

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "telco_churn_clean.csv"
)


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


df = load_data()


# --------------------------------------------------
# Generate customer risk predictions
# --------------------------------------------------

@st.cache_data
def generate_risk_data(df):

    # Remove columns that were not used during training
    X = df.drop(
        columns=["Churn", "customerID"]
    )

    # Predict churn probabilities
    probabilities = model.predict_proba(X)[:, 1]

    # Create risk table
    risk_df = pd.DataFrame({
        "Customer ID": df["customerID"],
        "Churn Probability": probabilities,
        "Risk Level": [
            get_risk_level(probability)
            for probability in probabilities
        ],
        "Monthly Revenue": df["MonthlyCharges"]
    })

    # Expected monthly revenue at risk
    risk_df["Revenue at Risk"] = (
        risk_df["Churn Probability"]
        * risk_df["Monthly Revenue"]
    )

    # Convert probability to percentage for dashboard display
    risk_df["Churn Probability"] = (
        risk_df["Churn Probability"] * 100
    )

    return risk_df


risk_df = generate_risk_data(df)


# --------------------------------------------------
# Portfolio KPIs
# --------------------------------------------------

high_risk_customers = (
    risk_df["Risk Level"] == "High"
).sum()

total_revenue_at_risk = (
    risk_df["Revenue at Risk"].sum()
)

average_probability = (
    risk_df["Churn Probability"].mean()
)


c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "High-Risk Customers",
        f"{high_risk_customers:,}"
    )

with c2:
    st.metric(
        "Expected Monthly Revenue Risk",
        f"${total_revenue_at_risk:,.0f}"
    )

with c3:
    st.metric(
        "Average Churn Probability",
        f"{average_probability:.1f}%"
    )


# --------------------------------------------------
# Retention Priority Queue
# --------------------------------------------------

st.markdown("## Retention Priority Queue")

st.caption(
    "Filter customers by predicted risk and prioritize "
    "retention efforts based on expected revenue exposure."
)


# --------------------------------------------------
# Filters
# --------------------------------------------------

filter_col1, filter_col2 = st.columns(2)

with filter_col1:

    risk_filter = st.multiselect(
        "Risk Level",
        ["High", "Medium", "Low"],
        default=["High"]
    )


with filter_col2:

    min_probability = st.slider(
        "Minimum Churn Probability",
        min_value=0,
        max_value=100,
        value=40,
        step=5
    )


# --------------------------------------------------
# Apply filters
# --------------------------------------------------

filtered = risk_df[
    (
        risk_df["Risk Level"].isin(
            risk_filter
        )
    )
    &
    (
        risk_df["Churn Probability"]
        >= min_probability
    )
].copy()


# Highest financial risk first
filtered = filtered.sort_values(
    "Revenue at Risk",
    ascending=False
)


# --------------------------------------------------
# Filter summary
# --------------------------------------------------

st.markdown(
    f"**{len(filtered):,} customers** match the current filters."
)


# --------------------------------------------------
# Customer risk table
# --------------------------------------------------

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True,
    column_config={

        "Churn Probability":
            st.column_config.ProgressColumn(
                "Churn Probability",
                help="Predicted probability that the customer will churn.",
                min_value=0,
                max_value=100,
                format="%.1f%%"
            ),

        "Monthly Revenue":
            st.column_config.NumberColumn(
                "Monthly Revenue",
                format="$%.2f"
            ),

        "Revenue at Risk":
            st.column_config.NumberColumn(
                "Revenue at Risk",
                help=(
                    "Churn probability multiplied by "
                    "monthly customer revenue."
                ),
                format="$%.2f"
            )
    }
)


# --------------------------------------------------
# Export retention list
# --------------------------------------------------

csv = filtered.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="Export Retention List",
    data=csv,
    file_name="retention_priority_customers.csv",
    mime="text/csv",
    use_container_width=True
)