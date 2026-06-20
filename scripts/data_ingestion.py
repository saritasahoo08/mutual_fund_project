import pandas as pd

# Load all 10 CSV files
print("Loading CSV files...")

df1 = pd.read_csv("data/raw/01_fund_master.csv")
df2 = pd.read_csv("data/raw/02_nav_history.csv")
df3 = pd.read_csv("data/raw/03_aum_by_fund_house.csv")
df4 = pd.read_csv("data/raw/04_monthly_sip_inflows.csv")
df5 = pd.read_csv("data/raw/05_category_inflows.csv")
df6 = pd.read_csv("data/raw/06_industry_folio_count.csv")
df7 = pd.read_csv("data/raw/07_scheme_performance.csv")
df8 = pd.read_csv("data/raw/08_investor_transactions.csv")
df9 = pd.read_csv("data/raw/09_portfolio_holdings.csv")
df10 = pd.read_csv("data/raw/10_benchmark_indices.csv")

# Print details for each file
print("\n1. Fund Master")
print("Shape:", df1.shape)
print("Columns:", df1.dtypes)
print(df1.head())

print("\n2. NAV History")
print("Shape:", df2.shape)
print("Columns:", df2.dtypes)
print(df2.head())

print("\n3. AUM by Fund House")
print("Shape:", df3.shape)
print("Columns:", df3.dtypes)
print(df3.head())

print("\n4. Monthly SIP Inflows")
print("Shape:", df4.shape)
print("Columns:", df4.dtypes)
print(df4.head())

print("\n5. Category Inflows")
print("Shape:", df5.shape)
print("Columns:", df5.dtypes)
print(df5.head())

print("\n6. Industry Folio Count")
print("Shape:", df6.shape)
print("Columns:", df6.dtypes)
print(df6.head())

print("\n7. Scheme Performance")
print("Shape:", df7.shape)
print("Columns:", df7.dtypes)
print(df7.head())

print("\n8. Investor Transactions")
print("Shape:", df8.shape)
print("Columns:", df8.dtypes)
print(df8.head())

print("\n9. Portfolio Holdings")
print("Shape:", df9.shape)
print("Columns:", df9.dtypes)
print(df9.head())

print("\n10. Benchmark Indices")
print("Shape:", df10.shape)
print("Columns:", df10.dtypes)
print(df10.head())

# Check for missing values
print("\nChecking for missing values...")
print("Fund Master missing:", df1.isnull().sum().sum())
print("NAV History missing:", df2.isnull().sum().sum())

# Explore fund_master
print("\nUnique Fund Houses:")
print(df1['fund_house'].unique())
print("Total:", df1['fund_house'].nunique())

print("\nUnique Categories:")
print(df1['category'].unique())

print("\nUnique Sub-Categories:")
print(df1['sub_category'].unique())

print("\nUnique Risk Grades:")
print(df1['risk_category'].unique())

# AMFI Code validation
print("\n=== AMFI CODE VALIDATION ===")
codes_in_master = df1['amfi_code'].unique()
codes_in_nav = df2['amfi_code'].unique()

print("Codes in fund_master:", len(codes_in_master))
print("Codes in nav_history:", len(codes_in_nav))

# Check if all master codes exist in nav
missing_codes = []
for code in codes_in_master:
    if code not in codes_in_nav:
        missing_codes.append(code)

if len(missing_codes) > 0:
    print("Missing codes:", missing_codes)
else:
    print("All codes in master exist in nav_history")

print("\nData ingestion complete!")