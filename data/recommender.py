import pandas as pd
import sqlite3

# connect to database
conn = sqlite3.connect("data/db/bluestock_mf.db")

# load data
fund_master = pd.read_sql("SELECT * FROM dim_fund", conn)
performance = pd.read_sql("SELECT * FROM fact_performance", conn)

# check columns
print("performance columns:", list(performance.columns))
print("fund_master columns:", list(fund_master.columns))

def recommend_funds(risk_appetite):
    # map risk appetite to actual risk grades in our data
    risk_map = {
        'Low':      ['Low'],
        'Moderate': ['Moderate', 'Moderately High'],
        'High':     ['High', 'Very High']
    }
    
    matching_grades = risk_map.get(risk_appetite, ['Moderate'])
    
    # filter performance data
    filtered = performance[performance['risk_grade'].isin(matching_grades)].copy()
    print(f"funds found with matching risk grade: {len(filtered)}")
    
    if len(filtered) == 0:
        print(f"no funds found for {risk_appetite} risk!")
        return
    
    # sort by sharpe ratio
    filtered = filtered.sort_values('sharpe_ratio', ascending=False)
    
    # get top 3
    top3 = filtered.head(3)
    
    print(f"\ntop 3 funds for {risk_appetite} risk:")
    print("-" * 50)
    
    for i, (_, row) in enumerate(top3.iterrows(), 1):
        # get fund name from fund_master separately
        code = row['amfi_code']
        fund_info = fund_master[fund_master['amfi_code'] == code]
        
        if len(fund_info) > 0:
            name = fund_info['scheme_name'].values[0]
            house = fund_info['fund_house'].values[0]
            category = fund_info['category'].values[0]
        else:
            name = f"Fund {code}"
            house = "Unknown"
            category = "Unknown"
        
        print(f"{i}. {name}")
        print(f"   fund house  : {house}")
        print(f"   category    : {category}")
        print(f"   sharpe ratio: {row['sharpe_ratio']:.2f}")
        print(f"   3yr return  : {row['return_3yr_pct']:.2f}%")
        print()
    
    return top3

# run recommender
print("mutual fund recommender")
print("=" * 50)
risk = input("enter risk appetite (Low / Moderate / High): ")
recommend_funds(risk)