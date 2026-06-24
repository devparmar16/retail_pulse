import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Inventory Optimization",
    page_icon="📦",
    layout="wide"
)

from utils.load_data import resolve_path

inventory_df = pd.read_csv(
    resolve_path("../notebooks/data/processed/inventory_optimization_results.csv")
)


# ----------------------------------
# TITLE
# ----------------------------------

st.title("📦 Inventory Optimization")

st.markdown(
    """
    Optimize inventory levels using ABC Analysis, EOQ, Safety Stock,
    and Reorder Point calculations.
    """
)

# ----------------------------------
# KPI SECTION
# ----------------------------------

total_products = len(inventory_df)

a_products = len(
    inventory_df[
        inventory_df["abc_category"] == "A"
    ]
)

critical_items = len(
    inventory_df[
        inventory_df["inventory_priority"] == "Critical"
    ]
)

avg_reorder = (
    inventory_df["reorder_point"]
    .mean()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Products",
    f"{total_products:,}"
)

col2.metric(
    "A Category Products",
    f"{a_products:,}"
)

col3.metric(
    "Critical Items",
    f"{critical_items:,}"
)

col4.metric(
    "Avg Reorder Point",
    f"{avg_reorder:,.0f}"
)

# ----------------------------------
# ABC ANALYSIS
# ----------------------------------

st.divider()

st.subheader(
    "ABC Inventory Analysis"
)

abc_counts = (
    inventory_df["abc_category"]
    .value_counts()
    .reset_index()
)

abc_counts.columns = [
    "category",
    "count"
]

fig = px.pie(
    abc_counts,
    names="category",
    values="count",
    hole=0.4
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# INVENTORY PRIORITY
# ----------------------------------

st.divider()

st.subheader(
    "Inventory Priority Breakdown"
)

priority_counts = (
    inventory_df["inventory_priority"]
    .value_counts()
    .reset_index()
)

priority_counts.columns = [
    "priority",
    "count"
]

fig = px.bar(
    priority_counts,
    x="priority",
    y="count",
    text="count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# TOP REORDER PRODUCTS
# ----------------------------------

st.divider()

st.subheader(
    "Highest Reorder Point Products"
)

top_reorder = (
    inventory_df
    .sort_values(
        "reorder_point",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top_reorder[
        [
            "stock_code",
            "description",
            "abc_category",
            "inventory_priority",
            "avg_daily_demand",
            "reorder_point"
        ]
    ],
    use_container_width=True
)

# ----------------------------------
# EOQ ANALYSIS
# ----------------------------------

st.divider()

st.subheader(
    "Economic Order Quantity (EOQ)"
)

top_eoq = (
    inventory_df
    .sort_values(
        "eoq",
        ascending=False
    )
    .head(20)
)

fig = px.bar(
    top_eoq,
    x="description",
    y="eoq"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# SAFETY STOCK ANALYSIS
# ----------------------------------

st.divider()

st.subheader(
    "Safety Stock Distribution"
)

fig = px.histogram(
    inventory_df,
    x="safety_stock",
    nbins=40
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# PRODUCT SEARCH
# ----------------------------------

st.divider()

st.subheader(
    "Product Search"
)

search_term = st.text_input(
    "Search Product"
)

if search_term:

    filtered = inventory_df[
        inventory_df["description"]
        .astype(str)
        .str.contains(
            search_term,
            case=False,
            na=False
        )
    ]

    st.dataframe(
        filtered,
        use_container_width=True
    )

# ----------------------------------
# INVENTORY EXPLORER
# ----------------------------------

st.divider()

st.subheader(
    "Inventory Explorer"
)

selected_category = st.selectbox(
    "ABC Category",
    ["All", "A", "B", "C"]
)

filtered_df = inventory_df.copy()

if selected_category != "All":

    filtered_df = filtered_df[
        filtered_df["abc_category"]
        == selected_category
    ]

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ----------------------------------
# DOWNLOAD
# ----------------------------------

st.divider()

st.download_button(
    "Download Inventory Plan",
    inventory_df.to_csv(index=False),
    "inventory_optimization_results.csv",
    "text/csv"
)