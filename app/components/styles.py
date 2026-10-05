import streamlit as st


def load_css():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0b1120;
        }

        .block-container {
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        h1, h2, h3 {
            letter-spacing: -0.025em;
        }

        .subtitle {
            color: #94a3b8;
            font-size: 1.05rem;
            margin-top: -12px;
            margin-bottom: 30px;
        }

        .metric-card {
            background: #111827;
            border: 1px solid #1f2937;
            border-radius: 14px;
            padding: 22px;
            min-height: 130px;
        }

        .metric-label {
            color: #94a3b8;
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.06em;
        }

        .metric-value {
            color: #f8fafc;
            font-size: 2rem;
            font-weight: 700;
            margin-top: 7px;
        }

        .metric-caption {
            color: #64748b;
            font-size: 0.8rem;
            margin-top: 5px;
        }

        .insight-card {
            background: #111827;
            border: 1px solid #1f2937;
            border-radius: 14px;
            padding: 20px;
            min-height: 145px;
        }

        .risk-high {
            background: rgba(239, 68, 68, 0.10);
            border: 1px solid rgba(239, 68, 68, 0.35);
            padding: 20px;
            border-radius: 12px;
        }

        .risk-medium {
            background: rgba(245, 158, 11, 0.10);
            border: 1px solid rgba(245, 158, 11, 0.35);
            padding: 20px;
            border-radius: 12px;
        }

        .risk-low {
            background: rgba(34, 197, 94, 0.10);
            border: 1px solid rgba(34, 197, 94, 0.35);
            padding: 20px;
            border-radius: 12px;
        }

        [data-testid="stMetric"] {
            background: #111827;
            border: 1px solid #1f2937;
            padding: 18px;
            border-radius: 14px;
        }

        [data-testid="stSidebar"] {
            background-color: #080d18;
            border-right: 1px solid #1f2937;
        }

        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid #1f2937;
            border-radius: 12px;
            overflow: hidden;
        }

        hr {
            border-color: #1f2937;
        }

        footer {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title, description):
    st.title(title)

    st.markdown(
        f'<p class="subtitle">{description}</p>',
        unsafe_allow_html=True,
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
        unsafe_allow_html=True,
    )