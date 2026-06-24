import pandas as pd

df = pd.read_csv(
    "../data/processed/inventory_optimization_results.csv"
)

print(df.columns.tolist())