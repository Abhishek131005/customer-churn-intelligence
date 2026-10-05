from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from app.components.styles import load_css


st.set_page_config(
    page_title="Churn Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()


st.markdown("# Customer Churn Intelligence")

st.markdown("""
<div class="subtitle">
Machine-learning powered customer retention and revenue-risk intelligence.
</div>
""", unsafe_allow_html=True)


st.markdown("""
### Turn churn predictions into retention decisions

This platform combines customer analytics, machine learning and
revenue-risk modelling to help identify customers most likely to leave
and prioritize retention efforts.
""")


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">PREDICT</div>
        <div class="metric-value">Churn Risk</div>
        <div class="metric-caption">
        Estimate customer-level churn probability.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">UNDERSTAND</div>
        <div class="metric-value">Risk Drivers</div>
        <div class="metric-caption">
        Understand factors influencing customer churn.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">PRIORITIZE</div>
        <div class="metric-value">Revenue</div>
        <div class="metric-caption">
        Identify customers representing the greatest revenue risk.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### Explore the platform")

st.markdown("""
Use the navigation menu to explore:

- **Overview** — executive-level customer and churn KPIs
- **Analytics** — explore behavioral churn patterns
- **Risk Center** — identify and prioritize high-risk customers
- **Prediction** — analyze an individual customer
- **Model Intelligence** — inspect model performance and drivers
""")