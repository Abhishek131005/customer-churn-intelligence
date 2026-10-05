from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

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
    "Customer Analytics",
    "Explore behavioral, service and financial patterns associated with churn."
)


# ---------------------------------
# Filter
# ---------------------------------

segment = st.selectbox(
    "Analyze churn by",
    [
        "Contract",
        "InternetService",
        "PaymentMethod",
        "TechSupport",
        "OnlineSecurity"
    ]
)


analysis = (
    df.assign(
        ChurnFlag=(df["Churn"] == "Yes").astype(int)
    )
    .groupby(segment)["ChurnFlag"]
    .agg(["mean", "count"])
    .reset_index()
)

analysis["mean"] *= 100

analysis.columns = [
    segment,
    "Churn Rate",
    "Customers"
]


fig = px.bar(
    analysis,
    x=segment,
    y="Churn Rate",
    text_auto=".1f",
    title=f"Churn Rate by {segment}"
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


st.markdown("## Customer Lifecycle")


left, right = st.columns(2)


with left:

    fig = px.histogram(
        df,
        x="tenure",
        color="Churn",
        nbins=30,
        title="Tenure Distribution by Churn"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with right:

    fig = px.box(
        df,
        x="Churn",
        y="MonthlyCharges",
        title="Monthly Charges by Churn Status"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )