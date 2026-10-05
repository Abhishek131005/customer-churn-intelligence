import streamlit as st


def load_css():
    st.markdown("""
    <style>

    /* Main page */
    .stApp {
        background: #0b1120;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Headings */
    h1, h2, h3 {
        letter-spacing: -0.02em;
    }

    /* Hero subtitle */
    .subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-top: -12px;
        margin-bottom: 28px;
    }

    /* KPI card */
    .metric-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 14px;
        padding: 22px;
        min-height: 125px;
    }

    .metric-label {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 2rem;
        font-weight: 700;
    }

    .metric-caption {
        color: #64748b;
        font-size: 0.78rem;
        margin-top: 5px;
    }

    /* Insight boxes */
    .insight-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
    }

    /* High risk */
    .risk-high {
        background: rgba(239,68,68,0.12);
        border: 1px solid rgba(239,68,68,0.35);
        padding: 18px;
        border-radius: 12px;
    }

    /* Medium risk */
    .risk-medium {
        background: rgba(245,158,11,0.12);
        border: 1px solid rgba(245,158,11,0.35);
        padding: 18px;
        border-radius: 12px;
    }

    /* Low risk */
    .risk-low {
        background: rgba(34,197,94,0.12);
        border: 1px solid rgba(34,197,94,0.35);
        padding: 18px;
        border-radius: 12px;
    }

    /* Streamlit metrics */
    [data-testid="stMetric"] {
        background: #111827;
        border: 1px solid #1f2937;
        padding: 16px;
        border-radius: 12px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #080d18;
        border-right: 1px solid #1f2937;
    }

    </style>
    """, unsafe_allow_html=True)


def page_header(title, description):
    st.title(title)

    st.markdown(
        f'<p class="subtitle">{description}</p>',
        unsafe_allow_html=True
    )


def metric_card(label, value, caption=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True
    )