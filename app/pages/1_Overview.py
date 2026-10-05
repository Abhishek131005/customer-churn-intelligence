from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from app.components.styles import (
    load_css,
    page_header,
    metric_card
)


load_css()

PROJECT_ROOT = Path(__file__).resolve().parents[2]

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


page_header(
    "Executive Overview",
    "A high-level view of customer churn, recurring revenue and retention risk."
)


# -----------------------------
# KPI calculations
# -----------------------------

customers = len(df)

churned = (
    df["Churn"] == "Yes"
).sum()

churn_rate = churned / customers

monthly_revenue = df["MonthlyCharges"].sum()

lost_monthly_revenue = df.loc[
    df["Churn"] == "Yes",
    "MonthlyCharges"
].sum()


# -----------------------------
# KPI row
# -----------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    metric_card(
        "TOTAL CUSTOMERS",
        f"{customers:,}",
        "Customers in portfolio"
    )

with c2:
    metric_card(
        "CHURN RATE",
        f"{churn_rate:.1%}",
        f"{churned:,} churned customers"
    )

with c3:
    metric_card(
        "MONTHLY REVENUE",
        f"${monthly_revenue:,.0f}",
        "Current customer portfolio"
    )

with c4:
    metric_card(
        "REVENUE LOST",
        f"${lost_monthly_revenue:,.0f}",
        "Monthly charges from churned customers"
    )


st.markdown("## Customer Risk Landscape")


left, right = st.columns(2)


# -----------------------------
# Churn distribution
# -----------------------------

with left:

    churn_counts = (
        df["Churn"]
        .value_counts()
        .reset_index()
    )

    churn_counts.columns = [
        "Churn",
        "Customers"
    ]

    fig = px.pie(
        churn_counts,
        names="Churn",
        values="Customers",
        hole=0.65,
        title="Customer Retention vs Churn"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# -----------------------------
# Contract churn
# -----------------------------

with right:

    contract = (
        df.assign(
            ChurnFlag=(df["Churn"] == "Yes").astype(int)
        )
        .groupby("Contract")["ChurnFlag"]
        .mean()
        .mul(100)
        .reset_index()
    )

    contract.columns = [
        "Contract",
        "Churn Rate"
    ]

    fig = px.bar(
        contract,
        x="Contract",
        y="Churn Rate",
        title="Churn Rate by Contract Type"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    st.markdown("## Key Business Insights")

i1, i2, i3 = st.columns(3)

with i1:
    st.markdown("""
    <div class="insight-card">
    <strong>Contract Risk</strong><br><br>
    Month-to-month customers represent the most vulnerable
    contract segment and should receive greater retention attention.
    </div>
    """, unsafe_allow_html=True)

with i2:
    st.markdown("""
    <div class="insight-card">
    <strong>Early Lifecycle Risk</strong><br><br>
    Customers with shorter tenure demonstrate substantially
    greater churn vulnerability than long-term customers.
    </div>
    """, unsafe_allow_html=True)

with i3:
    st.markdown("""
    <div class="insight-card">
    <strong>Revenue Exposure</strong><br><br>
    Churn should be prioritized using both customer probability
    and financial value rather than probability alone.
    </div>
    """, unsafe_allow_html=True)