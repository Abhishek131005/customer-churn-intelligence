from pathlib import Path
import sys

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from app.components.styles import load_css


st.set_page_config(
    page_title="Churn Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


load_css()


# --------------------------------------------------
# Sidebar branding
# --------------------------------------------------

with st.sidebar:
    st.markdown("## ◈ Churn Intelligence")

    st.caption(
        "ML-powered customer retention platform"
    )

    st.markdown("---")

    st.markdown(
        """
        **Production Model**  
        Logistic Regression
        """
    )

    st.markdown(
        """
        **System**  
        Streamlit + FastAPI
        """
    )

    st.markdown(
        """
        **Status**  
        🟢 Operational
        """
    )

    st.markdown("---")

    st.caption(
        "Customer Churn & Revenue Intelligence Platform"
    )


# --------------------------------------------------
# Hero
# --------------------------------------------------

st.markdown(
    "# Customer Churn Intelligence"
)

st.markdown(
    """
    <div class="subtitle">
    Predict churn. Understand customer risk. Protect recurring revenue.
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    This platform combines **customer analytics, machine learning,
    explainable predictions and revenue-risk modeling** to help
    retention teams identify customers most likely to leave and
    prioritize intervention.
    """
)


st.markdown("")


# --------------------------------------------------
# Product capabilities
# --------------------------------------------------

c1, c2, c3 = st.columns(3)


with c1:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">PREDICT</div>
            <div class="metric-value">Churn Risk</div>
            <div class="metric-caption">
                Estimate customer-level churn probability
                using the production ML pipeline.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with c2:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">UNDERSTAND</div>
            <div class="metric-value">Risk Drivers</div>
            <div class="metric-caption">
                Explore customer behaviors and model factors
                associated with churn.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with c3:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">PRIORITIZE</div>
            <div class="metric-value">Revenue</div>
            <div class="metric-caption">
                Rank customers using churn probability
                and expected revenue exposure.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown("---")


# --------------------------------------------------
# Navigation explanation
# --------------------------------------------------

st.markdown("## Explore the Platform")


left, right = st.columns(2)


with left:
    st.markdown(
        """
        ### Executive Intelligence

        **Overview**  
        Monitor churn KPIs, revenue exposure and customer
        lifecycle patterns.

        **Analytics**  
        Explore churn across contracts, services, payment
        methods and customer behavior.

        **Risk Center**  
        Identify high-risk customers and export prioritized
        retention lists.
        """
    )


with right:
    st.markdown(
        """
        ### Machine Learning

        **Prediction**  
        Analyze an individual customer using the deployed
        prediction API.

        **Model Intelligence**  
        Inspect model performance, decision thresholds and
        the strongest drivers of churn.
        """
    )


st.markdown("---")


st.caption(
    "Built with Python · Scikit-learn · FastAPI · "
    "Streamlit · Plotly"
)