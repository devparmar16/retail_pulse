import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Retail Analytics Platform",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# SIDEBAR PRODUCTION UPLOADER (GLOBAL STATE)
# -----------------------------
st.sidebar.header("📥 Ingestion Control")
uploaded_file = st.sidebar.file_uploader(
    "Upload Production Sales Data (CSV)", 
    type=["csv"]
)

# Manage global session memory for persistent multi-page uploads
if uploaded_file is not None:
    raw_upload = pd.read_csv(uploaded_file)
    raw_upload.columns = raw_upload.columns.str.strip()
    
    # Structural pipeline column name mapping
    rename_dict = {
        "InvoiceNo": "invoice_no", "StockCode": "stock_code", 
        "Description": "description", "Quantity": "quantity", 
        "InvoiceDate": "invoice_date", "UnitPrice": "unit_price", 
        "CustomerID": "customer_id", "Country": "country"
    }
    raw_upload.rename(columns=rename_dict, errors="ignore", inplace=True)
    
    # Calculate transaction boundaries inline
    raw_upload["quantity"] = pd.to_numeric(raw_upload["quantity"], errors="coerce")
    raw_upload["unit_price"] = pd.to_numeric(raw_upload["unit_price"], errors="coerce")
    raw_upload["total_amount"] = raw_upload["quantity"] * raw_upload["unit_price"]
    
    # Push parsed dataframe into persistent state memory
    st.session_state["sales_df"] = raw_upload[(raw_upload["quantity"] > 0) & (raw_upload["unit_price"] > 0)].copy()
    st.sidebar.success("Production data loaded into global session!")

elif "sales_df" not in st.session_state:
    # Baseline historical file fallback if session state is empty
    from utils.load_data import resolve_path
    st.session_state["sales_df"] = pd.read_csv(resolve_path("../notebooks/data/processed/cleaned_online_retail_all_sales.csv"))


# Bind current view data reference to active session state pool
sales_df = st.session_state["sales_df"]

# Load secondary analytical modeling metrics
from utils.load_data import resolve_path
rfm_df = pd.read_csv(resolve_path("../notebooks/data/processed/customer_rfm_features.csv"))
segment_df = pd.read_csv(resolve_path("../notebooks/data/processed/customer_segments.csv"))
monthly_sales = pd.read_csv(resolve_path("../notebooks/data/processed/eda_monthly_sales.csv"))


# -----------------------------
# TITLE
# -----------------------------
st.title("📊 Retail Analytics Platform")
st.markdown("""
Executive Dashboard for Retail Analytics Operations
""")
st.divider()

# -----------------------------
# KPI SECTION (Dynamically updates based on global session data)
# -----------------------------
total_revenue = sales_df["total_amount"].sum()
total_customers = int(sales_df["customer_id"].nunique())
total_orders = int(sales_df["invoice_no"].nunique())
total_products = int(sales_df["stock_code"].nunique())

col1, col2, col3, col4 = st.columns(4)
col1.metric("Revenue", f"${total_revenue:,.0f}")
col2.metric("Customers", f"{total_customers:,}")
col3.metric("Orders", f"{total_orders:,}")
col4.metric("Products", f"{total_products:,}")

# -----------------------------
# MONTHLY REVENUE TREND
# -----------------------------
st.divider()
st.subheader("📈 Monthly Revenue Trend")

fig = px.line(
    monthly_sales,
    x="year_month",
    y="monthly_revenue",
    markers=True,
    title="Revenue Timeline View"
)
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# CUSTOMER SEGMENTS
# -----------------------------
st.divider()
st.subheader("👥 Customer Segment Distribution")

segment_counts = (
    segment_df["business_segment"]
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

# -----------------------------
# TOP CUSTOMERS
# -----------------------------
st.divider()
st.subheader("💰 Top Customers by Revenue")

top_customers = (
    rfm_df
    .sort_values("monetary_capped", ascending=False)
    .head(10)
)
st.dataframe(
    top_customers[
        [
            "customer_id",
            "monetary_capped",
            "frequency",
            "rfm_score",
            "rfm_segment"
        ]
    ],
    use_container_width=True
)

# -----------------------------
# DATASET SUMMARY
# -----------------------------
st.divider()
st.subheader("📋 Dataset Summary")

summary_df = pd.DataFrame(
    {
        "Metric": ["Rows", "Customers", "Products", "Countries"],
        "Value": [
            len(sales_df),
            sales_df["customer_id"].nunique(),
            sales_df["stock_code"].nunique(),
            sales_df["country"].nunique()
        ]
    }
)
st.dataframe(summary_df, use_container_width=True)