import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Churn Prediction",
    page_icon="⚠️",
    layout="wide"
)

from utils.load_data import resolve_path

churn_df = pd.read_csv(
    resolve_path("../notebooks/data/processed/churn_prediction_results.csv")
)

feature_df = pd.read_csv(
    resolve_path("../notebooks/data/processed/churn_feature_importance.csv")
)

comparison_df = pd.read_csv(
    resolve_path("../notebooks/data/processed/churn_model_comparison.csv")
)


# -----------------------------------
# TITLE
# -----------------------------------

st.title("⚠️ Customer Churn Prediction")

st.markdown(
    """
    Identify customers at risk of leaving and understand the drivers behind churn.
    """
)

# -----------------------------------
# KPIs
# -----------------------------------

total_customers = len(churn_df)

predicted_churners = (
    churn_df["predicted_churn"]
    .sum()
)

churn_rate = (
    predicted_churners
    / total_customers
) * 100

high_risk_customers = len(
    churn_df[
        churn_df["blended_churn_probability"] >= 0.70
    ]
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Customers",
    f"{total_customers:,}"
)

col2.metric(
    "Predicted Churn Rate",
    f"{churn_rate:.1f}%"
)

col3.metric(
    "High Risk Customers",
    f"{high_risk_customers:,}"
)

# -----------------------------------
# CHURN PROBABILITY DISTRIBUTION
# -----------------------------------

st.divider()

st.subheader(
    "Churn Probability Distribution"
)

fig = px.histogram(
    churn_df,
    x="blended_churn_probability",
    nbins=30,
    title="Distribution of Churn Probabilities"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# FEATURE IMPORTANCE
# -----------------------------------

st.divider()

st.subheader(
    "Feature Importance"
)

feature_df = (
    feature_df
    .sort_values(
        "importance",
        ascending=True
    )
)

fig = px.bar(
    feature_df.tail(15),
    x="importance",
    y="feature",
    orientation="h",
    title="Top Churn Drivers"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# MODEL COMPARISON
# -----------------------------------

st.divider()

st.subheader(
    "Model Comparison"
)

st.dataframe(
    comparison_df,
    use_container_width=True
)

fig = px.bar(
    comparison_df,
    x="model",
    y="f1_score",
    title="Model F1 Score Comparison"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# HIGH RISK CUSTOMERS
# -----------------------------------

st.divider()

st.subheader(
    "High Risk Customers"
)

threshold = st.slider(
    "Probability Threshold",
    min_value=0.50,
    max_value=1.00,
    value=0.70,
    step=0.05
)

high_risk = churn_df[
    churn_df["blended_churn_probability"]
    >= threshold
]

st.write(
    f"Customers above threshold: {len(high_risk)}"
)

st.dataframe(
    high_risk.sort_values(
        "blended_churn_probability",
        ascending=False
    ),
    use_container_width=True
)

# -----------------------------------
# CUSTOMER LOOKUP
# -----------------------------------

st.divider()

st.subheader(
    "Customer Risk Explorer"
)

row_id = st.number_input(
    "Select Customer Record",
    min_value=0,
    max_value=len(churn_df) - 1,
    value=0
)

st.dataframe(
    churn_df.iloc[[row_id]],
    use_container_width=True
)

# -----------------------------------
# DOWNLOAD
# -----------------------------------

st.divider()

st.download_button(
    label="Download High Risk Customers",
    data=high_risk.to_csv(index=False),
    file_name="high_risk_customers.csv",
    mime="text/csv"
)