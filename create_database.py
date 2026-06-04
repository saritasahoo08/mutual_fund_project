import pandas as pd
from sqlalchemy import create_engine
import os

print("\n" + "="*60)
print("CREATING MUTUAL FUND DATABASE")
print("="*60 + "\n")

# Create the database file location
db_path = "data/db/bluestock_mf.db"

# Create a connection to SQLite
engine = create_engine(f'sqlite:///{db_path}')

print("Reading cleaned data files...\n")

# Read all cleaned CSV files we created
fund_master = pd.read_csv("data/processed/01_fund_master.csv")
nav_clean = pd.read_csv("data/processed/nav_history_clean.csv")
trans_clean = pd.read_csv("data/processed/investor_transactions_clean.csv")
perf_clean = pd.read_csv("data/processed/scheme_performance_clean.csv")
aum_data = pd.read_csv("data/raw/03_aum_by_fund_house.csv")

print("All files read successfully!\n")

# ===== LOAD INTO DATABASE =====

print("Loading data into database tables...\n")

# Load fund master (dimension table)
print("1. Loading Fund Master table...")
print(f"   Rows: {len(fund_master)}")
fund_master.to_sql('dim_fund', engine, if_exists='replace', index=False)
print("   ✓ Done\n")

# Load NAV history (fact table)
print("2. Loading NAV History table...")
print(f"   Rows: {len(nav_clean)}")
nav_clean.to_sql('fact_nav', engine, if_exists='replace', index=False)
print("   ✓ Done\n")

# Load transactions (fact table)
print("3. Loading Transactions table...")
print(f"   Rows: {len(trans_clean)}")
trans_clean.to_sql('fact_transactions', engine, if_exists='replace', index=False)
print("   ✓ Done\n")

# Load performance (fact table)
print("4. Loading Performance table...")
print(f"   Rows: {len(perf_clean)}")
perf_clean.to_sql('fact_performance', engine, if_exists='replace', index=False)
print("   ✓ Done\n")

# Load AUM (fact table)
print("5. Loading AUM table...")
print(f"   Rows: {len(aum_data)}")
aum_data.to_sql('fact_aum', engine, if_exists='replace', index=False)
print("   ✓ Done\n")

# Verify database was created
if os.path.exists(db_path):
    file_size = os.path.getsize(db_path) / (1024 * 1024)  # Convert to MB
    print("="*60)
    print("✓ DATABASE CREATED SUCCESSFULLY!")
    print("="*60)
    print(f"\nDatabase location: {db_path}")
    print(f"Database size: {file_size:.2f} MB")
    print(f"\nTables created:")
    print(f"  • dim_fund ({len(fund_master)} schemes)")
    print(f"  • fact_nav ({len(nav_clean)} price records)")
    print(f"  • fact_transactions ({len(trans_clean)} transactions)")
    print(f"  • fact_performance ({len(perf_clean)} metrics)")
    print(f"  • fact_aum ({len(aum_data)} AUM records)")
else:
    print("ERROR: Database was not created!")