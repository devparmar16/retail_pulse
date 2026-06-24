import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Customer Segmentation",
    page_icon="👥",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------

segments_df = pd.read_csv(
    "../notebooks/data/processed/customer_segments.csv"
)

summary_df = pd.read_csv(
    "../notebooks/data/processed/customer_segment_summary.csv"
)

interpretation_df = pd.read_csv(
    "../notebooks/data/processed/customer_segment_interpretation.csv"
)

# -----------------------------
# TITLE
# -----------------------------

st.title("👥 Customer Segmentation")

st.markdown(
    """
    Customer segmentation using K-Means clustering.
    """
)

# -----------------------------
# SEGMENT COUNTS
# -----------------------------

st.subheader("Segment Distribution")

segment_counts = (
    segments_df["business_segment"]
    .value_counts()
    .reset_index()
)

segment_counts.columns = [
    "business_segment",
    "count"
]

fig = px.pie(
    segment_counts,
    names="business_segment",
    values="count",
    hole=0.4
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# PCA VISUALIZATION
# -----------------------------

st.subheader("Cluster Visualization (PCA)")

fig = px.scatter(
    segments_df,
    x="pca_1",
    y="pca_2",
    color="business_segment",
    hover_data=[
        "customer_id",
        "frequency",
        "monetary_capped",
        "rfm_score"
    ]
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# CLUSTER SUMMARY
# -----------------------------

st.subheader("Cluster Summary")

st.dataframe(
    summary_df,
    use_container_width=True
)

# -----------------------------
# BUSINESS INTERPRETATION
# -----------------------------

st.subheader("Business Interpretation")

st.dataframe(
    interpretation_df,
    use_container_width=True
)

# -----------------------------
# CUSTOMER LOOKUP
# -----------------------------

st.subheader("Customer Lookup")

customer_id = st.selectbox(
    "Select Customer",
    sorted(
        segments_df["customer_id"]
        .unique()
    )
)

customer_data = segments_df[
    segments_df["customer_id"]
    == customer_id
]

st.dataframe(
    customer_data[
        [
            "customer_id",
            "business_segment",
            "frequency",
            "monetary_capped",
            "rfm_score"
        ]
    ],
    use_container_width=True
)