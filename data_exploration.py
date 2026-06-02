import pandas as pd

print("=== DATA EXPLORATION ===\n")

# Load the main files
fund_master = pd.read_csv("data/raw/01_fund_master.csv")
nav_history = pd.read_csv("data/raw/02_nav_history.csv")

# Explore fund_master
print("FUND MASTER EXPLORATION")
print(f"Total schemes: {len(fund_master)}")
print(f"Total columns: {len(fund_master.columns)}")

print("\nFund Houses:")
for house in fund_master['fund_house'].unique():
    count = len(fund_master[fund_master['fund_house'] == house])
    print(f"  {house}: {count} schemes")

print("\nCategories:")
for cat in fund_master['category'].unique():
    count = len(fund_master[fund_master['category'] == cat])
    print(f"  {cat}: {count} schemes")

print("\nSub-Categories:")
for subcat in fund_master['sub_category'].unique():
    count = len(fund_master[fund_master['sub_category'] == subcat])
    print(f"  {subcat}: {count} schemes")

print("\nRisk Categories:")
for risk in fund_master['risk_category'].unique():
    count = len(fund_master[fund_master['risk_category'] == risk])
    print(f"  {risk}: {count} schemes")

print("\nAMFI Code Range:")
print(f"  Min: {fund_master['amfi_code'].min()}")
print(f"  Max: {fund_master['amfi_code'].max()}")
print(f"  Total unique codes: {fund_master['amfi_code'].nunique()}")

print("\nExpense Ratio:")
print(f"  Min: {fund_master['expense_ratio_pct'].min()}%")
print(f"  Max: {fund_master['expense_ratio_pct'].max()}%")
print(f"  Average: {fund_master['expense_ratio_pct'].mean():.2f}%")

# Validate AMFI codes
print("\n=== AMFI CODE VALIDATION ===")

master_codes = set(fund_master['amfi_code'].unique())
nav_codes = set(nav_history['amfi_code'].unique())

print(f"Codes in fund_master: {len(master_codes)}")
print(f"Codes in nav_history: {len(nav_codes)}")

# Check if all master codes have nav data
missing_codes = master_codes - nav_codes
if len(missing_codes) > 0:
    print(f"\nCodes in master but not in nav: {missing_codes}")
else:
    print("\nAll codes in master have nav data!")

# Check for extra codes in nav
extra_codes = nav_codes - master_codes
if len(extra_codes) > 0:
    print(f"Extra codes in nav (not in master): {len(extra_codes)}")
else:
    print("No extra codes in nav")

# Data quality summary
print("\n=== DATA QUALITY SUMMARY ===")
print(f"Fund master null values: {fund_master.isnull().sum().sum()}")
print(f"Nav history null values: {nav_history.isnull().sum().sum()}")
print(f"Coverage: {len(master_codes & nav_codes)}/{len(master_codes)} schemes have nav data")

print("\nData quality looks good!")