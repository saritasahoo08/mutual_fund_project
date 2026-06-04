-- Bluestock Mutual Fund Database Schema
-- This file creates the structure for our database

-- Table 1: Fund Information
-- This stores basic details about each mutual fund scheme
CREATE TABLE dim_fund (
    amfi_code INTEGER PRIMARY KEY,      -- Unique code for each scheme
    fund_house TEXT,                    -- Name of fund company
    scheme_name TEXT,                   -- Full scheme name
    category TEXT,                      -- Type: Equity, Debt, Hybrid
    sub_category TEXT,                  -- Subcategory like Large Cap, Debt, etc
    plan TEXT,                          -- Direct or Regular plan
    launch_date DATE,                   -- When scheme was launched
    benchmark TEXT,                     -- Comparison benchmark index
    expense_ratio_pct REAL,             -- Annual charges (%)
    exit_load_pct REAL,                 -- Penalty if you withdraw early (%)
    min_sip_amount INTEGER,             -- Minimum monthly investment
    min_lumpsum_amount INTEGER,         -- Minimum one-time investment
    fund_manager TEXT,                  -- Who manages the fund
    risk_category TEXT,                 -- Risk level (Low, Medium, High)
    sebi_category_code TEXT             -- Government category code
);

-- Table 2: NAV Price History
-- This stores daily NAV (Net Asset Value) prices
CREATE TABLE fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-generated ID
    amfi_code INTEGER NOT NULL,                -- Which fund
    date DATE NOT NULL,                        -- Which date
    nav REAL,                                  -- Price on that date
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Table 3: All investor transactions
-- Tracks every buy/sell/redemption transaction
CREATE TABLE fact_transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id TEXT,                    -- Who invested
    transaction_date DATE NOT NULL,      -- When they invested
    amfi_code INTEGER NOT NULL,          -- Which fund
    transaction_type TEXT,               -- SIP, LUMPSUM, REDEMPTION
    amount_inr INTEGER,                  -- How much money
    state TEXT,                          -- Which state
    city TEXT,                           -- Which city
    city_tier TEXT,                      -- City size (Tier 1, 2, 3)
    age_group TEXT,                      -- Age bracket of investor
    gender TEXT,                         -- M or F
    annual_income_lakh REAL,             -- Yearly income
    payment_mode TEXT,                   -- How they paid
    kyc_status TEXT,                     -- KYC verification status
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Table 4: Fund performance metrics
-- Returns, risk metrics, ratings
CREATE TABLE fact_performance (
    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER NOT NULL,
    return_1yr_pct REAL,                 -- Returns in last 1 year (%)
    return_3yr_pct REAL,                 -- Returns in last 3 years (%)
    return_5yr_pct REAL,                 -- Returns in last 5 years (%)
    benchmark_3yr_pct REAL,              -- Benchmark returns (%)
    alpha REAL,                          -- Extra returns vs benchmark
    beta REAL,                           -- Volatility relative to market
    sharpe_ratio REAL,                   -- Risk-adjusted returns
    sortino_ratio REAL,                  -- Risk-adjusted returns (downside)
    std_dev_ann_pct REAL,                -- Annual volatility (%)
    max_drawdown_pct REAL,               -- Max loss from peak (%)
    aum_crore INTEGER,                   -- Assets Under Management in crores
    morningstar_rating INTEGER,          -- Rating out of 5
    risk_grade TEXT,                     -- Risk grade A-E
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Table 5: AUM by fund house
-- Total assets managed by each company per month
CREATE TABLE fact_aum (
    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    fund_house TEXT,
    aum_lakh_crore REAL,                 -- Total AUM in lakh crores
    aum_crore INTEGER,                   -- Total AUM in crores
    num_schemes INTEGER                  -- Number of schemes
);

-- Create indexes for faster queries
-- Helps database find data quickly
CREATE INDEX idx_nav_code ON fact_nav(amfi_code);
CREATE INDEX idx_nav_date ON fact_nav(date);
CREATE INDEX idx_trans_code ON fact_transactions(amfi_code);
CREATE INDEX idx_trans_state ON fact_transactions(state);