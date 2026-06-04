# Data Dictionary - Bluestock Mutual Fund Database

## Database Overview
This database contains mutual fund data including schemes, NAV history, investor transactions, performance metrics, and AUM data.

---

## TABLE 1: dim_fund (Dimensions - Fund Information)

| Column Name | Data Type | Description | Example |
|---|---|---|---|
| amfi_code | INTEGER | Unique identifier for each mutual fund scheme | 125497 |
| fund_house | TEXT | Name of the asset management company | HDFC Mutual Fund |
| scheme_name | TEXT | Full name of the fund scheme | HDFC Top 100 Fund |
| category | TEXT | Fund category (Equity/Debt/Hybrid) | Equity |
| sub_category | TEXT | More specific category | Large Cap |
| plan | TEXT | Investment plan type | Direct |
| launch_date | DATE | Date when scheme was launched | 2005-01-01 |
| benchmark | TEXT | Index used for comparison | Nifty 100 |
| expense_ratio_pct | REAL | Annual management fee (%) | 0.50 |
| exit_load_pct | REAL | Early withdrawal penalty (%) | 0.00 |
| min_sip_amount | INTEGER | Minimum monthly SIP amount (₹) | 500 |
| min_lumpsum_amount | INTEGER | Minimum one-time investment (₹) | 5000 |
| fund_manager | TEXT | Name of fund manager | John Doe |
| risk_category | TEXT | Risk level | High |
| sebi_category_code | TEXT | Government classification code | 2020/10-14 |

---

## TABLE 2: fact_nav (Facts - NAV Price History)

| Column Name | Data Type | Description | Example |
|---|---|---|---|
| nav_id | INTEGER | Auto-generated unique ID | 1 |
| amfi_code | INTEGER | Fund identifier (links to dim_fund) | 125497 |
| date | DATE | Date of NAV price | 2024-01-15 |
| nav | REAL | Net Asset Value (price per unit) | 250.50 |

**Source**: 02_nav_history.csv (46,000 records)
**Date Range**: 2022-01-03 to 2026-05-29

---

## TABLE 3: fact_transactions (Facts - Investor Transactions)

| Column Name | Data Type | Description | Example |
|---|---|---|---|
| transaction_id | INTEGER | Unique transaction ID | 1 |
| investor_id | TEXT | Investor identifier | INV123456 |
| transaction_date | DATE | Date of transaction | 2024-01-15 |
| amfi_code | INTEGER | Fund identifier | 125497 |
| transaction_type | TEXT | Type (SIP/LUMPSUM/REDEMPTION) | SIP |
| amount_inr | INTEGER | Investment amount in Rupees | 10000 |
| state | TEXT | State of investor | Maharashtra |
| city | TEXT | City of investor | Mumbai |
| city_tier | TEXT | City size classification | Tier 1 |
| age_group | TEXT | Age bracket | 30-40 |
| gender | TEXT | Gender | M/F |
| annual_income_lakh | REAL | Yearly income in lakhs | 25.5 |
| payment_mode | TEXT | How payment was made | Bank Transfer |
| kyc_status | TEXT | KYC verification status | Verified |

**Source**: 08_investor_transactions.csv (32,778 records)

---

## TABLE 4: fact_performance (Facts - Fund Performance Metrics)

| Column Name | Data Type | Description | Example |
|---|---|---|---|
| performance_id | INTEGER | Unique ID | 1 |
| amfi_code | INTEGER | Fund identifier | 125497 |
| return_1yr_pct | REAL | Returns in last 1 year (%) | 15.5 |
| return_3yr_pct | REAL | Returns in last 3 years (%) ANNUALIZED | 18.2 |
| return_5yr_pct | REAL | Returns in last 5 years (%) ANNUALIZED | 16.8 |
| benchmark_3yr_pct | REAL | Benchmark index returns (%) | 14.5 |
| alpha | REAL | Excess return vs benchmark | 3.7 |
| beta | REAL | Volatility relative to market | 1.2 |
| sharpe_ratio | REAL | Risk-adjusted returns | 1.5 |
| sortino_ratio | REAL | Downside risk-adjusted returns | 2.1 |
| std_dev_ann_pct | REAL | Annual volatility (%) | 12.3 |
| max_drawdown_pct | REAL | Maximum loss from peak (%) | -25.5 |
| aum_crore | INTEGER | Assets Under Management in crores (₹) | 5000 |
| morningstar_rating | INTEGER | Rating out of 5 stars | 5 |
| risk_grade | TEXT | Risk grade (A=Low, E=High) | B |

**Source**: 07_scheme_performance.csv (40 records)

---

## TABLE 5: fact_aum (Facts - AUM by Fund House)

| Column Name | Data Type | Description | Example |
|---|---|---|---|
| aum_id | INTEGER | Unique ID | 1 |
| date | DATE | Date of AUM snapshot | 2024-01-31 |
| fund_house | TEXT | Name of fund company | HDFC Mutual Fund |
| aum_lakh_crore | REAL | Total AUM in lakh crores (₹) | 3.5 |
| aum_crore | INTEGER | Total AUM in crores (₹) | 350000 |
| num_schemes | INTEGER | Number of schemes managed | 45 |

**Source**: 03_aum_by_fund_house.csv (90 records)

---

## Key Metrics Explained

### Alpha
- Shows if fund outperformed its benchmark
- Positive alpha = fund did better than expected
- Example: Alpha of 3% means fund beat benchmark by 3%

### Beta
- Measures how much fund moves vs market
- Beta = 1.0 means fund moves same as market
- Beta = 1.2 means fund is 20% more volatile

### Sharpe Ratio
- Risk-adjusted returns
- Higher is better
- Typical: 0.5 to 2.0

### Sortino Ratio
- Like Sharpe but only counts downside risk
- Better for downside protection analysis

### Max Drawdown
- Worst loss from peak to trough
- Example: -25% means worst loss was 25%

---

## Data Quality Notes

- **NAV**: Forward-filled for weekends/holidays
- **Transactions**: Validated amount > 0
- **Performance**: Returns are annualized percentages
- **AUM**: In crores (1 crore = 10 million Rupees)