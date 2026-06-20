import pandas as pd
import numpy as np

print("\nStarting data cleaning...\n")

# ===== CLEANING NAV HISTORY =====
print("Step 1: Cleaning NAV History")
print("-" * 50)

# Read the NAV file
nav_df = pd.read_csv("data/raw/02_nav_history.csv")
print(f"Original rows: {len(nav_df)}")

# Convert date column to proper date format (the dates are in YYYY-MM-DD format)
nav_df['date'] = pd.to_datetime(nav_df['date'])

# Convert nav column to number (in case there are text values)
nav_df['nav'] = pd.to_numeric(nav_df['nav'], errors='coerce')

# Sort by amfi_code first, then by date
# This makes it easier to work with time series data
nav_df = nav_df.sort_values(['amfi_code', 'date']).reset_index(drop=True)

# Remove exact duplicates (same code and date)
nav_df = nav_df.drop_duplicates(subset=['amfi_code', 'date'], keep='first')

# Forward fill missing NAV values
# When market is closed (weekend/holiday), we use the previous day's NAV
nav_df['nav'] = nav_df.groupby('amfi_code')['nav'].ffill()

# Remove rows where NAV is 0 or negative (invalid data)
nav_df = nav_df[nav_df['nav'] > 0]

print(f"Cleaned rows: {len(nav_df)}")
print(f"Date range: {nav_df['date'].min()} to {nav_df['date'].max()}")

# Save cleaned file
nav_df.to_csv("data/processed/nav_history_clean.csv", index=False)
print("Saved: data/processed/nav_history_clean.csv\n")

# ===== CLEANING INVESTOR TRANSACTIONS =====
print("Step 2: Cleaning Investor Transactions")
print("-" * 50)

# Read transactions file
trans_df = pd.read_csv("data/raw/08_investor_transactions.csv")
print(f"Original rows: {len(trans_df)}")

# Clean up transaction type (remove spaces and make uppercase)
trans_df['transaction_type'] = trans_df['transaction_type'].str.strip().str.upper()

# Check what transaction types we have
print(f"Transaction types found: {trans_df['transaction_type'].unique()}")

# Remove invalid transactions (amount must be greater than 0)
trans_df = trans_df[trans_df['amount_inr'] > 0]

# Convert transaction date to proper date format
trans_df['transaction_date'] = pd.to_datetime(trans_df['transaction_date'])

# Check KYC status values
print(f"KYC status values: {trans_df['kyc_status'].unique()}")

print(f"Cleaned rows: {len(trans_df)}")

# Save cleaned file
trans_df.to_csv("data/processed/investor_transactions_clean.csv", index=False)
print("Saved: data/processed/investor_transactions_clean.csv\n")

# ===== CLEANING SCHEME PERFORMANCE =====
print("Step 3: Cleaning Scheme Performance")
print("-" * 50)

# Read performance file
perf_df = pd.read_csv("data/raw/07_scheme_performance.csv")
print(f"Original rows: {len(perf_df)}")

# Convert return columns to numbers
return_columns = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct', 'benchmark_3yr_pct']
for col in return_columns:
    perf_df[col] = pd.to_numeric(perf_df[col], errors='coerce')

# Check for unusual expense ratios
# Normal range is 0.1% to 2.5%
unusual = perf_df[(perf_df['expense_ratio_pct'] < 0.1) | (perf_df['expense_ratio_pct'] > 2.5)]
if len(unusual) > 0:
    print(f"WARNING: Found {len(unusual)} schemes with unusual expense ratios:")
    for idx, row in unusual.iterrows():
        print(f"  - {row['scheme_name']}: {row['expense_ratio_pct']}%")

print(f"Cleaned rows: {len(perf_df)}")

# Save cleaned file
perf_df.to_csv("data/processed/scheme_performance_clean.csv", index=False)
print("Saved: data/processed/scheme_performance_clean.csv\n")

print("=" * 50)
print("All data cleaning completed!")
print("=" * 50)