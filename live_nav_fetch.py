import requests
import pandas as pd
import os
from datetime import datetime

print("="*70)
print("FETCHING LIVE NAV DATA FROM MFAPI.IN")
print("="*70)

# Make sure output folder exists
os.makedirs("data/raw", exist_ok=True)

# 5 key schemes to fetch + HDFC Top 100
schemes = {
    "HDFC_Top_100_Direct":    125497,
    "SBI_Bluechip":           119551,
    "ICICI_Bluechip":         120503,
    "Nippon_Large_Cap":       118632,
    "Axis_Bluechip":          119092,
    "Kotak_Bluechip":         120841,
}

all_nav_data = []

for scheme_name, scheme_code in schemes.items():
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    
    print(f"\n{'='*70}")
    print(f"Fetching: {scheme_name} (Code: {scheme_code})")
    print(f"{'='*70}")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract metadata
        meta = data['meta']
        print(f"✅ Fund House: {meta['fund_house']}")
        print(f"✅ Scheme Name: {meta['scheme_name']}")
        
        # Extract NAV history
        nav_data = data['data']
        print(f"✅ Records fetched: {len(nav_data)}")
        print(f"✅ Latest NAV: {nav_data[0]['nav']} on {nav_data[0]['date']}")
        
        # Create DataFrame
        df = pd.DataFrame(nav_data)
        df['scheme_code'] = scheme_code
        df['scheme_name'] = scheme_name
        df['fund_house'] = meta['fund_house']
        df['fetch_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Save individual CSV
        filename = f"data/raw/live_{scheme_name}_nav.csv"
        df.to_csv(filename, index=False)
        print(f"✅ Saved: {filename}")
        print(f"   Shape: {df.shape}")
        
        all_nav_data.append(df)
        
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR fetching {scheme_name}: {str(e)}")
        continue
    except Exception as e:
        print(f"❌ ERROR processing {scheme_name}: {str(e)}")
        continue

# Combine all NAV data
if len(all_nav_data) > 0:
    combined_df = pd.concat(all_nav_data, ignore_index=True)
    
    print(f"\n{'='*70}")
    print("COMBINED LIVE NAV DATA SUMMARY")
    print(f"{'='*70}")
    print(f"\nTotal records: {len(combined_df)}")
    print(f"Total schemes: {combined_df['scheme_code'].nunique()}")
    print(f"Date range: {combined_df['date'].min()} to {combined_df['date'].max()}")
    
    print(f"\nFirst 5 rows:")
    print(combined_df.head())
    
    print(f"\nData types:")
    print(combined_df.dtypes)
    
    # Save combined CSV
    combined_df.to_csv("data/raw/live_all_schemes_nav.csv", index=False)
    print(f"\n✅ Combined data saved: data/raw/live_all_schemes_nav.csv")
    
    print(f"\n{'='*70}")
    print("LIVE NAV FETCH COMPLETE ✅")
    print(f"{'='*70}\n")
else:
    print("\n❌ No data was fetched successfully")