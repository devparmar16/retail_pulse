import pandas as pd
import numpy as np

def run_production_pipeline(uploaded_file):
    """
    Ingests raw user CSV transaction records and formats them to fit 
    the exact schemas required by your Streamlit dashboard pages.
    """
    # 1. Ingestion & Clean Parsing
    df = pd.read_csv(uploaded_file)
    
    # Strip whitespace from column targets safely
    df.columns = df.columns.str.strip()
    
    # Map raw names if lowercase or alternative formats are uploaded
    rename_dict = {
        "InvoiceNo": "invoice_no", "StockCode": "stock_code", 
        "Description": "description", "Quantity": "quantity", 
        "InvoiceDate": "invoice_date", "UnitPrice": "unit_price", 
        "CustomerID": "customer_id", "Country": "country"
    }
    df.rename(columns=rename_dict, errors="ignore", inplace=True)
    
    # Enforce strict types
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["total_amount"] = df["quantity"] * df["unit_price"]
    
    # Clear out structural nulls/cancelled lines for calculations
    clean_sales = df[(df["quantity"] > 0) & (df["unit_price"] > 0)].copy()
    
    return clean_sales