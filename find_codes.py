import requests

print("Fetching official AMFI fund list... please wait...\n")

# AMFI official fund list
url = "https://www.amfiindia.com/spages/NAVAll.txt"
response = requests.get(url)
lines = response.text.split('\n')

keywords = ["hdfc top 100", "sbi bluechip", "axis bluechip", "kotak bluechip"]

print(f"Total lines fetched: {len(lines)}\n")

for line in lines:
    line_lower = line.lower()
    for keyword in keywords:
        if keyword in line_lower:
            print(f"FOUND: {line.strip()}")