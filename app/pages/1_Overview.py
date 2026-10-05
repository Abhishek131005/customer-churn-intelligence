from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from app.components.styles import (
    load_css,
    page_header,
    metric_card,
)


load_css()


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
    "Monitor customer churn, recurring revenue and key retention signals.",
)


# --------------------------------------------------
# KPI calculations
# --------------------------------------------------

total_customers = len(df)

churned_customers = (
    df["Churn"] == "Yes"
).sum()

churn_rate = (
    churned_customers / total_customers
)

monthly_revenue = (
    df["MonthlyCharges"].sum()
)

lost_monthly_revenue = (
    df.loc[
        df["Churn"] == "Yes",
        "MonthlyCharges",
    ].sum()
)


# --------------------------------------------------
# KPI cards
# --------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    metric_card(
        "TOTAL CUSTOMERS",
        f"{total_customers:,}",
        "Customers analyzed",
    )

with c2:
    metric_card(
        "CHURN RATE",
        f"{churn_rate:.1%}",
        f"{churned_customers:,} churned customers",
    )

with c3:
    metric_card(
        "MONTHLY REVENUE",
        f"${monthly_revenue:,.0f}",
        "Customer portfolio",
    )

with c4:
    metric_card(
        "REVENUE LOST",
        f"${lost_monthly_revenue:,.0f}",
        "Monthly charges from churned customers",
    )


st.markdown("## Customer Risk Landscape")


# --------------------------------------------------
# Charts
# --------------------------------------------------

left, right = st.columns(2)


with left:
    churn_counts = (
        df["Churn"]
        .value_counts()
        .reset_index()
    )

    churn_counts.columns = [
        "Churn",
        "Customers",
    ]

    fig = px.pie(
        churn_counts,
        names="Churn",
        values="Customers",
        hole=0.68,
        title="Retention vs Churn",
        color="Churn",
        color_discrete_map={
            "No": "#6366F1",
            "Yes": "#EF4444",
        },
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text="",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


with right:
    contract = (
        df.assign(
            ChurnFlag=(
                df["Churn"] == "Yes"
            ).astype(int)
        )
        .groupby("Contract")["ChurnFlag"]
        .mean()
        .mul(100)
        .reset_index()
    )

    contract.columns = [
        "Contract",
        "Churn Rate",
    ]

    fig = px.bar(
        contract,
        x="Contract",
        y="Churn Rate",
        text_auto=".1f",
        title="Churn Rate by Contract",
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis_title="Churn Rate (%)",
        xaxis_title="",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# --------------------------------------------------
# Customer lifecycle
# --------------------------------------------------

st.markdown("## Customer Lifecycle Risk")


tenure_df = df.copy()

tenure_df["Tenure Group"] = pd.cut(
    tenure_df["tenure"],
    bins=[-1, 6, 12, 24, 48, 72],
    labels=[
        "0–6 months",
        "7–12 months",
        "13–24 months",
        "25–48 months",
        "49–72 months",
    ],
)


tenure_risk = (
    tenure_df.assign(
        ChurnFlag=(
            tenure_df["Churn"] == "Yes"
        ).astype(int)
    )
    .groupby(
        "Tenure Group",
        observed=True,
    )["ChurnFlag"]
    .mean()
    .mul(100)
    .reset_index()
)


fig = px.line(
    tenure_risk,
    x="Tenure Group",
    y="ChurnFlag",
    markers=True,
    title="Churn Risk Across Customer Lifecycle",
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis_title="Customer Tenure",
    yaxis_title="Churn Rate (%)",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)


# --------------------------------------------------
# Business insights
# --------------------------------------------------

st.markdown("## Key Business Insights")


i1, i2, i3 = st.columns(3)


with i1:
    st.markdown(
        """
        <div class="insight-card">
        <strong>Contract Risk</strong><br><br>
        Month-to-month customers demonstrate substantially
        greater churn vulnerability than customers on
        longer-term contracts.
        </div>
        """,
        unsafe_allow_html=True,
    )


with i2:
    st.markdown(
        """
        <div class="insight-card">
        <strong>Early Lifecycle Risk</strong><br><br>
        Churn risk is concentrated among newer customers,
        making early lifecycle engagement an important
        retention opportunity.
        </div>
        """,
        unsafe_allow_html=True,
    )


with i3:
    st.markdown(
        """
        <div class="insight-card">
        <strong>Revenue Prioritization</strong><br><br>
        Retention decisions should consider both churn
        probability and customer financial value rather
        than probability alone.
        </div>
        """,
        unsafe_allow_html=True,
    )