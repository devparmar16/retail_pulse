import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_sample_test_csv():
    np.random.seed(42)
    
    # 1. Base configuration
    num_rows = 150
    customers = [f"1{i:04d}" for i in range(10, 25)] # Sample production customer IDs
    stock_codes = ["85123A", "71053", "84406B", "84029G", "22720", "22197", "85099B"]
    descriptions = [
        "white hanging heart t-light holder",
        "white metal lantern",
        "cream cupid hearts coat hanger",
        "knitted union flag hot water bottle",
        "regency cakestand 3 tier",
        "popcorn holder",
        "jumbo bag red retrospot"
    ]
    countries = ["United Kingdom", "Germany", "France", "Spain"]
    
    # 2. Synthesize timeline arrays 
    start_date = datetime(2026, 1, 1)
    date_list = [start_date + timedelta(days=int(np.random.randint(0, 150))) for _ in range(num_rows)]
    
    # 3. Compile transaction matrices
    data = {
        "InvoiceNo": [f"58{np.random.randint(1000, 9999)}" for _ in range(num_rows)],
        "StockCode": [np.random.choice(stock_codes) for _ in range(num_rows)],
        "Quantity": [np.random.randint(1, 24) for _ in range(num_rows)],
        "InvoiceDate": [dt.strftime("%Y-%m-%d %H:%M:%S") for dt in date_list],
        "UnitPrice": [round(np.random.uniform(1.5, 12.5), 2) for _ in range(num_rows)],
        "CustomerID": [np.random.choice(customers) for _ in range(num_rows)],
        "Country": [np.random.choice(countries) for _ in range(num_rows)]
    }
    
    # Align descriptions to stock codes perfectly
    df = pd.DataFrame(data)
    code_to_desc = dict(zip(stock_codes, descriptions))
    df["Description"] = df["StockCode"].map(code_to_desc)
    
    # Add a few custom simulated canceled transactions to verify filtering robustness
    for i in range(5):
        df.loc[i, "InvoiceNo"] = "C" + df.loc[i, "InvoiceNo"]
        df.loc[i, "Quantity"] = -df.loc[i, "Quantity"]

    # 4. Save to root directory context
    df.to_csv("online_retail_test.csv", index=False)
    print("✨ 'online_retail_test.csv' successfully generated in your project root!")

if __name__ == "__main__":
    create_sample_test_csv()