import pandas as pd

try:
    df = pd.read_excel('d:\\SSA\\mothly.xlsx')
    print("Columns:", df.columns.tolist())
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nLength:", len(df))
except Exception as e:
    print("Error:", e)
