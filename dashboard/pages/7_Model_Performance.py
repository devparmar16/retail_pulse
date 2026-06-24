import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Model Performance",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 Model Performance Dashboard")
st.markdown("""
Centralized evaluation of all machine learning modules.
""")

# ==================================
# LOAD FILES
# ==================================
churn_df = pd.read_csv("../notebooks/data/processed/churn_model_comparison.csv")
clv_df = pd.read_csv("../notebooks/data/processed/clv_model_comparison.csv")
forecast_df = pd.read_csv("../notebooks/data/processed/demand_forecast_model_comparison.csv")
rules_df = pd.read_csv("../notebooks/data/processed/recommendation_association_rules.csv")
inventory_df = pd.read_csv("../notebooks/data/processed/inventory_optimization_results.csv")
segments_df = pd.read_csv("../notebooks/data/processed/customer_segments.csv")

# ==================================
# EXECUTIVE KPI
# ==================================
st.subheader("Executive Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Customers Segmented", f"{len(segments_df):,}")
col2.metric("Recommendation Rules", f"{len(rules_df):,}")
col3.metric("Inventory Products", f"{len(inventory_df):,}")
col4.metric(
    "Forecast Records",
    f"{len(pd.read_csv('../notebooks/data/processed/demand_forecast_results.csv')):,}"
)

# ==================================
# CHURN
# ==================================
st.divider()
st.subheader("⚠️ Churn Prediction")
st.dataframe(churn_df, use_container_width=True)

fig = px.bar(
    churn_df,
    x="model",
    y="f1_score",
    color="roc_auc",
    title="Churn Model Comparison"
)
st.plotly_chart(fig, use_container_width=True)

# ==================================
# CLV
# ==================================
st.divider()
st.subheader("💎 CLV Models")
st.dataframe(clv_df, use_container_width=True)

fig = px.bar(
    clv_df,
    x="model",
    y="R2",
    color="R2",
    title="CLV Regression Performance"
)
st.plotly_chart(fig, use_container_width=True)

# ==================================
# DEMAND FORECASTING
# ==================================
st.divider()
st.subheader("📈 Forecasting Models")
st.dataframe(forecast_df, use_container_width=True)

fig = px.bar(
    forecast_df,
    x="model",
    y="SMAPE",
    color="SMAPE",
    title="Forecasting Error Comparison"
)
st.plotly_chart(fig, use_container_width=True)

# ==================================
# SEGMENTATION
# ==================================
st.divider()
st.subheader("👥 Customer Segmentation")

segment_counts = (
    segments_df["business_segment"]
    .value_counts()
    .reset_index()
)
segment_counts.columns = ["business_segment", "count"]

fig = px.pie(
    segment_counts,
    names="business_segment",
    values="count",
    hole=0.4,
    title="Customer Segments Breakdown"
)
st.plotly_chart(fig, use_container_width=True)

# ==================================
# RECOMMENDATION ENGINE
# ==================================
st.divider()
st.subheader("🛒 Recommendation Engine")

col1, col2, col3 = st.columns(3)

col1.metric("Association Rules", len(rules_df))
col2.metric(
    "Strong Rules",
    len(pd.read_csv("../notebooks/data/processed/recommendation_strong_rules.csv"))
)
col3.metric(
    "Frequent Itemsets",
    len(pd.read_csv("../notebooks/data/processed/recommendation_frequent_itemsets.csv"))
)

# ==================================
# INVENTORY
# ==================================
st.divider()
st.subheader("📦 Inventory Optimization")
st.dataframe(inventory_df.head(10), use_container_width=True)

abc_counts = (
    inventory_df["abc_category"]
    .value_counts()
    .reset_index()
)
abc_counts.columns = ["category", "count"]

fig = px.bar(
    abc_counts,
    x="category",
    y="count",
    title="ABC Inventory Distribution",
    text_auto=True
)
st.plotly_chart(fig, use_container_width=True)

# ==================================
# OVERALL SCORECARD
# ==================================
st.divider()
st.subheader("Project Achievement Summary")

scorecard = pd.DataFrame({
    "Module": ["Segmentation", "Churn", "CLV", "Forecasting", "Recommendations", "Inventory"],
    "Status": ["Completed", "Completed", "Completed", "Completed", "Completed", "Completed"]
})
st.dataframe(scorecard, use_container_width=True)