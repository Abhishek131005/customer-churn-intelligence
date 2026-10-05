import plotly.express as px
import streamlit as st

from src.models.explain import get_feature_importance
from app.components.styles import load_css, page_header


load_css()


page_header(
    "Model Intelligence",
    "Understand model performance, interpretability and prediction methodology."
)


st.markdown("## Production Model")

st.markdown("""
**Logistic Regression**

Logistic Regression was selected after comparison with alternative
classification models because it provided the strongest overall
performance while maintaining high interpretability.

The production pipeline includes preprocessing and classification
inside a single reproducible Scikit-learn pipeline.
""")


st.markdown("## Why Not Accuracy Alone?")

st.markdown("""
Customer churn is an imbalanced classification problem. A model can
achieve deceptively high accuracy by predicting the majority class.

The system therefore evaluates **precision, recall, F1-score and
ROC-AUC**, with additional emphasis on recall because failing to
identify a genuine churner can result in lost recurring revenue.
""")


st.markdown("## Classification Threshold")

st.markdown("""
The production decision threshold was selected using the
precision-recall trade-off rather than automatically relying on the
default 0.50 threshold.
""")


st.markdown("## Most Influential Features")


importance = get_feature_importance()

top = importance.head(15).copy()

top["Direction"] = top["coefficient"].apply(
    lambda x:
    "Increases churn risk"
    if x > 0
    else "Reduces churn risk"
)


fig = px.bar(
    top.sort_values("coefficient"),
    x="coefficient",
    y="feature",
    orientation="h",
    color="Direction",
    title="Top Logistic Regression Coefficients"
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)