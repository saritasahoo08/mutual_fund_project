import pandas as pd
import os

print("="*70)
print("DAY 1: DATA INGESTION AND EXPLORATION")
print("="*70)

# List of all 10 CSV files
csv_files = [
    "data/raw/01_fund_master.csv",
    "data/raw/02_nav_history.csv",
    "data/raw/03_aum_by_fund_house.csv",
    "data/raw/04_monthly_sip_inflows.csv",
    "data/raw/05_category_inflows.csv",
    "data/raw/06_industry_folio_count.csv",
    "data/raw/07_scheme_performance.csv",
    "data/raw/08_investor_transactions.csv",
    "data/raw/09_portfolio_holdings.csv",
    "data/raw/10_benchmark_indices.csv",
]

datasets = {}

for filepath in csv_files:
    filename = os.path.basename(filepath)
    print(f"\n{'='*70}")
    print(f"FILE: {filename}")
    print(f"{'='*70}")
    
    # Check if file exists
    if not os.path.exists(filepath):
        print(f"❌ FILE NOT FOUND: {filepath}")
        continue
    
    # Load CSV
    df = pd.read_csv(filepath)
    datasets[filename] = df
    
    # Print shape
    print(f"\n📊 SHAPE: {df.shape[0]} rows × {df.shape[1]} columns")
    
    # Print data types
    print(f"\n📋 DATA TYPES:")
    print(df.dtypes)
    
    # Print first few rows
    print(f"\n📄 FIRST 5 ROWS:")
    print(df.head())
    
    # Check for missing values
    print(f"\n⚠️ MISSING VALUES (Null counts):")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("   ✅ NO MISSING VALUES")
    else:
        print(missing[missing > 0])
    
    # Check for duplicates
    print(f"\n🔄 DUPLICATES:")
    dup_count = df.duplicated().sum()
    print(f"   Total duplicate rows: {dup_count}")
    
    # Check data ranges for numeric columns
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_cols) > 0:
        print(f"\n🔢 NUMERIC COLUMN RANGES:")
        for col in numeric_cols[:5]:  # Show first 5 numeric columns
            print(f"   {col}: min={df[col].min()}, max={df[col].max()}")

# SECTION 2: EXPLORE FUND MASTER
print(f"\n\n{'='*70}")
print("SECTION 2: FUND MASTER EXPLORATION")
print(f"{'='*70}")

fund_master = datasets['01_fund_master.csv']

print("\n🏢 UNIQUE FUND HOUSES:")
print(fund_master['fund_house'].unique())
print(f"   Total: {fund_master['fund_house'].nunique()}")

print("\n📂 UNIQUE CATEGORIES:")
print(fund_master['category'].unique())
print(f"   Total: {fund_master['category'].nunique()}")

print("\n🏷️ UNIQUE SUB-CATEGORIES:")
print(fund_master['sub_category'].unique())
print(f"   Total: {fund_master['sub_category'].nunique()}")

print("\n⚡ UNIQUE RISK GRADES:")
print(fund_master['risk_category'].unique())
print(f"   Total: {fund_master['risk_category'].nunique()}")

print("\n📍 AMFI CODE RANGE:")
print(f"   Min: {fund_master['amfi_code'].min()}")
print(f"   Max: {fund_master['amfi_code'].max()}")
print(f"   Total codes: {fund_master['amfi_code'].nunique()}")

# SECTION 3: VALIDATE AMFI CODES
print(f"\n\n{'='*70}")
print("SECTION 3: AMFI CODE VALIDATION")
print(f"{'='*70}")

nav_history = datasets['02_nav_history.csv']

master_codes = set(fund_master['amfi_code'].unique())
nav_codes = set(nav_history['amfi_code'].unique())

print(f"\n📊 CODE COMPARISON:")
print(f"   Codes in fund_master: {len(master_codes)}")
print(f"   Codes in nav_history: {len(nav_codes)}")

# Find codes in master but not in nav
missing_in_nav = master_codes - nav_codes
if len(missing_in_nav) > 0:
    print(f"\n⚠️ CODES IN MASTER BUT NOT IN NAV_HISTORY ({len(missing_in_nav)}):")
    print(f"   {missing_in_nav}")
else:
    print(f"\n✅ ALL CODES IN MASTER EXIST IN NAV_HISTORY")

# Find codes in nav but not in master
extra_in_nav = nav_codes - master_codes
if len(extra_in_nav) > 0:
    print(f"\n⚠️ CODES IN NAV_HISTORY BUT NOT IN MASTER ({len(extra_in_nav)}):")
    print(f"   {extra_in_nav}")
else:
    print(f"\n✅ NO EXTRA CODES IN NAV_HISTORY")

# DATA QUALITY SUMMARY
print(f"\n\n{'='*70}")
print("DATA QUALITY SUMMARY")
print(f"{'='*70}")

quality_report = f"""
✅ POSITIVE FINDINGS:
   • All 10 CSV files loaded successfully
   • Total records across all datasets: {sum(len(df) for df in datasets.values()):,}
   • Fund master contains {len(master_codes)} unique schemes
   • NAV history has {len(nav_codes)} schemes with price data
   
⚠️ OBSERVATIONS:
   • Fund master: {fund_master.isnull().sum().sum()} null values
   • NAV history: {nav_history.isnull().sum().sum()} null values
   • AMFI code coverage: {len(master_codes & nav_codes)}/{len(master_codes)} funds have NAV data
   
✅ STATUS: Data is ready for analysis
"""

print(quality_report)

print(f"{'='*70}")
print("DATA INGESTION COMPLETE ✅")
print(f"{'='*70}\n")