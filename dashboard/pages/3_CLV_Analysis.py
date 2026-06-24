import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.metrics import accuracy_score

st.set_page_config(page_title="Customer Lifetime Value", page_icon="💎", layout="wide")

# ----------------------------------
# LOAD DATA
# ----------------------------------
clv_pred = pd.read_csv("../notebooks/data/processed/clv_predictions.csv")
feature_df = pd.read_csv("../notebooks/data/processed/clv_feature_importance.csv")
comparison_df = pd.read_csv("../notebooks/data/processed/clv_model_comparison.csv")
classification_df = pd.read_csv("../notebooks/data/processed/clv_classification_results.csv")

# Fix target mismatch if 'actual_category' was saved as continuous log values
if classification_df["actual_category"].dtype in [np.float64, np.float32]:
    # Dynamically convert continuous values back into 4 quartile bins (0 to 3) to match predictions
    classification_df["actual_category"] = pd.qcut(
        classification_df["actual_category"].rank(method="first"),
        q=4,
        labels=[0, 1, 2, 3]
    ).astype(int)

# Map numeric categories to readable string labels for visualization
class_mapping = {0: "Low Value", 1: "Medium Value", 2: "High Value", 3: "Very High Value"}
classification_df["actual_label"] = classification_df["actual_category"].map(class_mapping).fillna("Unknown")
classification_df["predicted_label"] = classification_df["predicted_category"].map(class_mapping).fillna("Unknown")

# ----------------------------------
# TITLE
# ----------------------------------
st.title("💎 Customer Lifetime Value Analysis")
st.markdown("""
Predict long-term customer value and identify high-value customer segments.
""")

# ----------------------------------
# KPI SECTION
# ----------------------------------
avg_clv = clv_pred["predicted_clv"].mean()
max_clv = clv_pred["predicted_clv"].max()
total_predicted_value = clv_pred["predicted_clv"].sum()

# Calculate accuracy safely using aligned categorical arrays
classification_accuracy = accuracy_score(
    classification_df["actual_category"], 
    classification_df["predicted_category"]
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Average CLV", f"${avg_clv:,.0f}")
col2.metric("Highest CLV", f"${max_clv:,.0f}")
col3.metric("Total Predicted Value", f"${total_predicted_value:,.0f}")
col4.metric("Classification Accuracy", f"{classification_accuracy:.2%}")

# ----------------------------------
# DISTRIBUTION
# ----------------------------------
st.divider()
st.subheader("📊 Predicted CLV Distribution")
fig = px.histogram(clv_pred, x="predicted_clv", nbins=40, title="Distribution of Customer Lifetime Value")
st.plotly_chart(fig, use_container_width=True)

# ----------------------------------
# ACTUAL VS PREDICTED
# ----------------------------------
st.divider()
st.subheader("🎯 Actual vs Predicted CLV (Regression)")
fig = px.scatter(clv_pred, x="actual_clv", y="predicted_clv", opacity=0.6, 
                 labels={"actual_clv": "Actual Value", "predicted_clv": "Predicted Value"},
                 title="Regression Fit Alignment")
st.plotly_chart(fig, use_container_width=True)

# ----------------------------------
# FEATURE IMPORTANCE
# ----------------------------------
st.divider()
st.subheader("💡 Key Value Drivers")
feature_df = feature_df.sort_values("importance", ascending=True)
fig = px.bar(feature_df, x="importance", y="feature", orientation="h", title="Feature Importance Metrics")
st.plotly_chart(fig, use_container_width=True)

# ----------------------------------
# MODEL COMPARISON
# ----------------------------------
st.divider()
st.subheader("🏁 Regression Model Performance")
st.dataframe(comparison_df, use_container_width=True)
fig = px.bar(comparison_df, x="model", y="R2", text="R2", title="R² Score Comparison")
st.plotly_chart(fig, use_container_width=True)

# ----------------------------------
# CLASSIFICATION SUMMARY
# ----------------------------------
st.divider()
st.subheader("🏷️ CLV Category Tier Breakdown")
actual_counts = classification_df["actual_label"].value_counts().reset_index()
actual_counts.columns = ["Value Tier", "Customer Count"]
fig = px.pie(actual_counts, names="Value Tier", values="Customer Count", hole=0.4, title="Actual Customer Tier Distribution")
st.plotly_chart(fig, use_container_width=True)

# ----------------------------------
# TOP CUSTOMERS
# ----------------------------------
st.divider()
st.subheader("👑 Top Predicted High-Value Customers")
top_customers = clv_pred.sort_values("predicted_clv", ascending=False).head(20)
st.dataframe(top_customers, use_container_width=True)

# ----------------------------------
# DOWNLOAD
# ----------------------------------
st.divider()
st.download_button("📥 Download CLV Predictions CSV", clv_pred.to_csv(index=False), "clv_predictions.csv", "text/csv")