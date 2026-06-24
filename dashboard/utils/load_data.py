import pandas as pd
import streamlit as st
import os

# Resolve paths dynamically relative to this file's location to prevent FileNotFoundError on Streamlit Cloud
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # goes up to dashboard/
project_root = os.path.dirname(base_dir) # goes up to project root

def resolve_path(relative_path):
    clean_path = relative_path.replace("../", "")
    return os.path.join(project_root, clean_path)


@st.cache_data
def load_customer_segments():
    return pd.read_csv(
        resolve_path("../notebooks/data/processed/customer_segments.csv")
    )


@st.cache_data
def load_churn_results():
    return pd.read_csv(
        resolve_path("../notebooks/data/processed/churn_prediction_results.csv")
    )


@st.cache_data
def load_rfm():
    return pd.read_csv(
        resolve_path("../notebooks/data/processed/customer_rfm_features.csv")
    )


@st.cache_data
def load_forecast():
    return pd.read_csv(
        resolve_path("../notebooks/data/processed/demand_forecast_results.csv")
    )


@st.cache_data
def load_inventory():
    return pd.read_csv(
        resolve_path("../notebooks/data/processed/inventory_optimization_results.csv")
    )


@st.cache_data
def load_sales():
    return pd.read_csv(
        resolve_path("../notebooks/data/processed/cleaned_online_retail_all_sales.csv")
    )