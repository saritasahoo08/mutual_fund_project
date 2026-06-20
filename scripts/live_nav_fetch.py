import requests
import pandas as pd

print("Fetching live NAV data...")

# List of schemes to fetch
schemes = {
    "HDFC_Top_100": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841,
}

# Fetch data for each scheme
for name, code in schemes.items():
    url = f"https://api.mfapi.in/mf/{code}"
    response = requests.get(url)
    data = response.json()
    
    print(f"\nFetching {name} (code: {code})")
    print(f"Fund House: {data['meta']['fund_house']}")
    print(f"Scheme Name: {data['meta']['scheme_name']}")
    print(f"Latest NAV: {data['data'][0]['nav']} on {data['data'][0]['date']}")
    
    # Convert to dataframe and save
    df = pd.DataFrame(data['data'])
    df['scheme_code'] = code
    df['scheme_name'] = name
    
    filename = f"data/raw/live_{name}_nav.csv"
    df.to_csv(filename, index=False)
    print(f"Saved to {filename}")
    print(f"Shape: {df.shape}")

print("\nLive NAV fetch complete!")