import pandas as pd
import streamlit as st


@st.cache_data
def load_customer_segments():
    return pd.read_csv(
        "../notebooks/data/processed/customer_segments.csv"
    )


@st.cache_data
def load_churn_results():
    return pd.read_csv(
        "../notebooks/data/processed/churn_prediction_results.csv"
    )


@st.cache_data
def load_rfm():
    return pd.read_csv(
        "../notebooks/data/processed/customer_rfm_features.csv"
    )


@st.cache_data
def load_forecast():
    return pd.read_csv(
        "../notebooks/data/processed/demand_forecast_results.csv"
    )


@st.cache_data
def load_inventory():
    return pd.read_csv(
        "../notebooks/data/processed/inventory_optimization_results.csv"
    )


@st.cache_data
def load_sales():
    return pd.read_csv(
        "../notebooks/data/processed/cleaned_online_retail_all_sales.csv"
    )