import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Demand Forecasting",
    page_icon="📈",
    layout="wide"
)

# ----------------------------------
# LOAD DATA
# ----------------------------------

forecast_df = pd.read_csv(
    "../notebooks/data/processed/demand_forecast_results.csv"
)

comparison_df = pd.read_csv(
    "../notebooks/data/processed/demand_forecast_model_comparison.csv"
)

feature_df = pd.read_csv(
    "../notebooks/data/processed/xgboost_forecast_feature_importance.csv"
)

# ----------------------------------
# TITLE
# ----------------------------------

st.title("📈 Demand Forecasting")

st.markdown(
    """
    Forecast future retail demand using machine learning and ensemble models.
    """
)

# ----------------------------------
# KPI SECTION
# ----------------------------------

best_model_row = comparison_df.sort_values(
    "MAE"
).iloc[0]

best_model = best_model_row["model"]

best_mae = best_model_row["MAE"]

best_rmse = best_model_row["RMSE"]

best_smape = best_model_row["SMAPE"]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Best Model",
    best_model
)

col2.metric(
    "MAE",
    f"{best_mae:,.0f}"
)

col3.metric(
    "RMSE",
    f"{best_rmse:,.0f}"
)

col4.metric(
    "SMAPE",
    f"{best_smape:.2f}%"
)

# ----------------------------------
# FORECAST CHART
# ----------------------------------

st.divider()

st.subheader(
    "Actual vs Forecasted Demand"
)

forecast_df["date"] = pd.to_datetime(
    forecast_df["date"]
)

model_choice = st.selectbox(
    "Choose Forecast Model",
    [
        "original_xgboost_prediction",
        "tuned_xgboost_prediction",
        "random_forest_prediction",
        "ensemble_prediction"
    ]
)

plot_df = forecast_df.copy()

fig = px.line(
    plot_df,
    x="date",
    y=[
        "actual_demand",
        model_choice
    ],
    title="Demand Forecast Comparison"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# MODEL COMPARISON
# ----------------------------------

st.divider()

st.subheader(
    "Forecast Model Comparison"
)

st.dataframe(
    comparison_df,
    use_container_width=True
)

fig = px.bar(
    comparison_df.sort_values(
        "MAE"
    ),
    x="model",
    y="MAE",
    text="MAE"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# FEATURE IMPORTANCE
# ----------------------------------

st.divider()

st.subheader(
    "Feature Importance"
)

feature_df = feature_df.sort_values(
    "importance",
    ascending=True
)

fig = px.bar(
    feature_df,
    x="importance",
    y="feature",
    orientation="h"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# FORECAST TABLE
# ----------------------------------

st.divider()

st.subheader(
    "Forecast Results"
)

st.dataframe(
    forecast_df.tail(50),
    use_container_width=True
)

# ----------------------------------
# DEMAND ERROR ANALYSIS
# ----------------------------------

st.divider()

st.subheader(
    "Forecast Error Analysis"
)

forecast_df["absolute_error"] = (
    forecast_df["actual_demand"]
    - forecast_df["ensemble_prediction"]
).abs()

fig = px.histogram(
    forecast_df,
    x="absolute_error",
    nbins=30,
    title="Absolute Forecast Error Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# DOWNLOAD
# ----------------------------------

st.divider()

st.download_button(
    "Download Forecast Results",
    forecast_df.to_csv(index=False),
    "forecast_results.csv",
    "text/csv"
)