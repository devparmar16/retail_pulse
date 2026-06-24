import pandas as pd
from pathlib import Path

folder = Path("./data/processed")

for csv_file in sorted(folder.glob("*.csv")):
    try:
        df = pd.read_csv(csv_file, low_memory=False)

        print("\n" + "=" * 80)
        print(f"FILE: {csv_file.name}")
        print(f"ROWS: {len(df)}")
        print(f"COLUMNS: {len(df.columns)}")

        if len(df.columns) <= 20:
            print("COLUMN NAMES:")
            for col in df.columns:
                print(f"  - {col}")
        else:
            print("FIRST 10 COLUMNS:")
            for col in df.columns[:10]:
                print(f"  - {col}")

            print("...")

            print("LAST 10 COLUMNS:")
            for col in df.columns[-10:]:
                print(f"  - {col}")

    except Exception as e:
        print(f"\nERROR reading {csv_file.name}: {e}")