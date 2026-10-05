import streamlit as st


st.set_page_config(
    page_title="Churn Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.title("Customer Churn Intelligence")

st.markdown(
    """
    Predict customer churn, understand behavioral
    risk factors, and identify revenue at risk.
    """
)


st.info(
    "Use the navigation menu to explore customer "
    "analytics, risk intelligence, and predictions."
)