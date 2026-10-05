from pathlib import Path
import sys

import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from app.components.styles import (
    load_css,
    page_header,
)

from src.models.explain import (
    get_feature_importance,
)


load_css()


page_header(
    "Model Intelligence",
    "Inspect the production model, decision methodology and key churn drivers.",
)


# --------------------------------------------------
# Model information
# --------------------------------------------------

st.markdown("## Production Model")

left, right = st.columns([2, 1])


with left:
    st.markdown(
        """
        ### Logistic Regression

        Logistic Regression was selected as the production
        classifier after comparison with Random Forest and
        XGBoost.

        The final model is packaged together with the complete
        preprocessing pipeline so raw customer attributes can
        be passed directly to the prediction system.
        """
    )


with right:
    st.info(
        "Production pipeline\n\n"
        "Preprocessing → Logistic Regression"
    )


# --------------------------------------------------
# IMPORTANT:
# Replace these values with YOUR ACTUAL notebook
# Logistic Regression results.
# --------------------------------------------------

ROC_AUC = 0.835929
RECALL = 0.572193
PRECISION = 0.648485
F1_SCORE = 0.607955

# Replace with your selected threshold.
DECISION_THRESHOLD = 0.40


st.markdown("## Model Performance")


c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "ROC-AUC",
    f"{ROC_AUC:.3f}",
)

c2.metric(
    "Recall",
    f"{RECALL:.3f}",
)

c3.metric(
    "Precision",
    f"{PRECISION:.3f}",
)

c4.metric(
    "F1 Score",
    f"{F1_SCORE:.3f}",
)


st.caption(
    "Replace the placeholder metric values in "
    "5_Model_Intelligence.py with the actual Logistic "
    "Regression results from 03_modeling.ipynb."
)


# --------------------------------------------------
# Evaluation explanation
# --------------------------------------------------

st.markdown("## Evaluation Strategy")

st.markdown(
    """
    Accuracy alone is not sufficient for customer churn
    prediction because churn is an imbalanced classification
    problem.

    The model was evaluated using **precision, recall,
    F1-score and ROC-AUC**.

    Recall is particularly important in this use case because
    false negatives represent customers who actually churn but
    are not identified for retention intervention.
    """
)


# --------------------------------------------------
# Threshold
# --------------------------------------------------

st.markdown("## Classification Threshold")


threshold_percentage = int(
    DECISION_THRESHOLD * 100
)


st.metric(
    "Production Decision Threshold",
    f"{threshold_percentage}%",
)


st.markdown(
    """
    Rather than automatically relying on the default 50%
    classification threshold, threshold analysis was performed
    to evaluate the trade-off between precision and recall.

    The production threshold should correspond to the threshold
    selected during the modeling experiment.
    """
)


# --------------------------------------------------
# Feature importance
# --------------------------------------------------

st.markdown("## Key Churn Drivers")


importance = get_feature_importance().copy()


def clean_feature_name(name):
    name = name.replace(
        "num__",
        "",
    )

    name = name.replace(
        "cat__",
        "",
    )

    replacements = {
        "MonthlyCharges": "Monthly Charges",
        "TotalCharges": "Total Charges",
        "SeniorCitizen": "Senior Citizen",
        "PaperlessBilling": "Paperless Billing",
        "PaymentMethod": "Payment Method",
        "InternetService": "Internet Service",
        "OnlineSecurity": "Online Security",
        "OnlineBackup": "Online Backup",
        "DeviceProtection": "Device Protection",
        "TechSupport": "Tech Support",
        "StreamingTV": "Streaming TV",
        "StreamingMovies": "Streaming Movies",
        "PhoneService": "Phone Service",
        "MultipleLines": "Multiple Lines",
    }

    for old, new in replacements.items():
        name = name.replace(
            old,
            new,
        )

    name = name.replace(
        "_",
        " · ",
    )

    return name


importance["Feature"] = (
    importance["feature"]
    .apply(clean_feature_name)
)


importance["Direction"] = (
    importance["coefficient"]
    .apply(
        lambda coefficient:
        "Increases churn risk"
        if coefficient > 0
        else "Reduces churn risk"
    )
)


top_features = (
    importance
    .sort_values(
        "importance",
        ascending=False,
    )
    .head(15)
    .sort_values(
        "coefficient",
        ascending=True,
    )
)


fig = px.bar(
    top_features,
    x="coefficient",
    y="Feature",
    orientation="h",
    color="Direction",
    title="Most Influential Logistic Regression Features",
    color_discrete_map={
        "Increases churn risk": "#EF4444",
        "Reduces churn risk": "#22C55E",
    },
)


fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=620,
    xaxis_title="Logistic Regression Coefficient",
    yaxis_title="",
    legend_title_text="",
)


st.plotly_chart(
    fig,
    use_container_width=True,
)


st.caption(
    "Positive coefficients push predictions toward churn. "
    "Negative coefficients push predictions toward retention."
)


# --------------------------------------------------
# Model comparison
# --------------------------------------------------

st.markdown("## Models Evaluated")

st.markdown(
    """
    During experimentation, three classification approaches
    were evaluated:

    - **Logistic Regression** — interpretable linear baseline
      and final production model.
    - **Random Forest** — nonlinear ensemble model capable of
      capturing feature interactions.
    - **XGBoost** — gradient-boosted tree model evaluated for
      stronger nonlinear predictive performance.

    Logistic Regression was retained as the final model based
    on the observed evaluation results and its strong
    interpretability for a customer-retention use case.
    """
)