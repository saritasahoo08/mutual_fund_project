-- Bluestock Mutual Fund - Analytical Queries
-- These queries help us understand the data and find insights

-- ===== QUERY 1: Top 5 Funds by AUM =====
-- Find which funds have the most money invested
SELECT 
    f.scheme_name,
    f.fund_house,
    p.aum_crore as total_aum_crore
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.aum_crore DESC
LIMIT 5;

-- ===== QUERY 2: Average NAV per Month =====
-- Calculate average price for each fund by month
SELECT 
    f.scheme_name,
    strftime('%Y-%m', n.date) as month,
    ROUND(AVG(n.nav), 2) as avg_nav,
    COUNT(*) as trading_days
FROM fact_nav n
JOIN dim_fund f ON n.amfi_code = f.amfi_code
GROUP BY f.scheme_name, month
ORDER BY f.scheme_name, month DESC
LIMIT 20;

-- ===== QUERY 3: SIP vs Lumpsum Transactions =====
-- Compare how many SIP and Lumpsum investments
SELECT 
    transaction_type,
    COUNT(*) as total_transactions,
    SUM(amount_inr) as total_amount,
    ROUND(AVG(amount_inr), 0) as avg_amount
FROM fact_transactions
GROUP BY transaction_type;

-- ===== QUERY 4: Transactions by State =====
-- Which states have the most investments?
SELECT 
    state,
    COUNT(*) as num_transactions,
    SUM(amount_inr) as total_amount,
    COUNT(DISTINCT investor_id) as unique_investors
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC
LIMIT 10;

-- ===== QUERY 5: Funds with Low Expense Ratio =====
-- Find funds that charge less than 1% fee
SELECT 
    scheme_name,
    fund_house,
    category,
    ROUND(expense_ratio_pct, 2) as expense_ratio
FROM dim_fund
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- ===== QUERY 6: Best Performing Funds (1 Year) =====
-- Which funds gave the highest returns in 1 year?
SELECT 
    f.scheme_name,
    f.fund_house,
    f.category,
    p.return_1yr_pct,
    p.sharpe_ratio,
    p.morningstar_rating
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.return_1yr_pct IS NOT NULL
ORDER BY p.return_1yr_pct DESC
LIMIT 10;

-- ===== QUERY 7: Fund House Market Share =====
-- Which fund houses manage the most money?
SELECT 
    fund_house,
    COUNT(DISTINCT amfi_code) as num_schemes,
    SUM(aum_crore) as total_aum_crore
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum_crore DESC
LIMIT 10;

-- ===== QUERY 8: Investor Demographics =====
-- Age group and gender distribution of investments
SELECT 
    age_group,
    gender,
    COUNT(*) as num_transactions,
    ROUND(AVG(amount_inr), 0) as avg_investment,
    SUM(amount_inr) as total_invested
FROM fact_transactions
GROUP BY age_group, gender
ORDER BY total_invested DESC;

-- ===== QUERY 9: High Risk vs Low Risk Allocation =====
-- How much money is invested in different risk categories?
SELECT 
    f.risk_category,
    COUNT(DISTINCT t.amfi_code) as num_funds,
    COUNT(*) as num_transactions,
    SUM(t.amount_inr) as total_amount
FROM fact_transactions t
JOIN dim_fund f ON t.amfi_code = f.amfi_code
WHERE f.risk_category IS NOT NULL
GROUP BY f.risk_category
ORDER BY total_amount DESC;

-- ===== QUERY 10: New vs Redemption Trends =====
-- Track how much money is coming in vs going out
SELECT 
    strftime('%Y-%m', transaction_date) as month,
    transaction_type,
    COUNT(*) as num_transactions,
    SUM(amount_inr) as total_amount
FROM fact_transactions
GROUP BY month, transaction_type
ORDER BY month DESC, transaction_type;