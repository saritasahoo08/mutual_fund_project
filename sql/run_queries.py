import sqlite3
import pandas as pd

print("\n" + "="*60)
print("RUNNING ANALYTICAL SQL QUERIES")
print("="*60 + "\n")

# Connect to database
conn = sqlite3.connect("data/db/bluestock_mf.db")

# Query 1: Top 5 funds by AUM
print("QUERY 1: Top 5 Funds by AUM")
print("-"*60)
q1 = """
SELECT 
    scheme_name,
    fund_house,
    aum_crore
FROM (
    SELECT DISTINCT
        f.scheme_name,
        f.fund_house,
        p.aum_crore
    FROM fact_performance p
    JOIN dim_fund f ON p.amfi_code = f.amfi_code
)
ORDER BY aum_crore DESC
LIMIT 5
"""
df1 = pd.read_sql_query(q1, conn)
print(df1.to_string(index=False))
print()

# Query 2: Funds with expense ratio < 1%
print("QUERY 2: Funds with Expense Ratio < 1%")
print("-"*60)
q2 = """
SELECT 
    scheme_name,
    fund_house,
    category,
    ROUND(expense_ratio_pct, 2) as expense_ratio
FROM dim_fund
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC
"""
df2 = pd.read_sql_query(q2, conn)
print(df2.to_string(index=False))
print()

# Query 3: Transactions by type
print("QUERY 3: Transactions by Type")
print("-"*60)
q3 = """
SELECT 
    transaction_type,
    COUNT(*) as num_transactions,
    SUM(amount_inr) as total_amount
FROM fact_transactions
GROUP BY transaction_type
"""
df3 = pd.read_sql_query(q3, conn)
print(df3.to_string(index=False))
print()

# Query 4: Top 10 states by investment
print("QUERY 4: Top 10 States by Investment Amount")
print("-"*60)
q4 = """
SELECT 
    state,
    COUNT(*) as num_transactions,
    SUM(amount_inr) as total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC
LIMIT 10
"""
df4 = pd.read_sql_query(q4, conn)
print(df4.to_string(index=False))
print()

# Query 5: Best performing funds (1 year)
print("QUERY 5: Best Performing Funds (1 Year)")
print("-"*60)
q5 = """
SELECT 
    f.scheme_name,
    f.fund_house,
    ROUND(p.return_1yr_pct, 2) as return_1yr,
    ROUND(p.sharpe_ratio, 2) as sharpe_ratio
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.return_1yr_pct IS NOT NULL
ORDER BY p.return_1yr_pct DESC
LIMIT 10
"""
df5 = pd.read_sql_query(q5, conn)
print(df5.to_string(index=False))
print()

print("="*60)
print("All queries executed successfully!")
print("="*60)

conn.close()