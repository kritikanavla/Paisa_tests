import requests
import json

API_BASE = "https://paisa.example.com/api"
SESSION_TOKEN = "ZyJ1aiWMTwXYLZpESbQJrPbVIqk9-3hkJA-PbfKM0zg"

def inspect_discovery():
    headers = {"Authorization": f"Bearer {SESSION_TOKEN}"}
    try:
        runs = requests.get(f"{API_BASE}/discovery/runs", headers=headers).json()
        if not runs: return
        latest_date = runs[0]['id']
        results = requests.get(f"{API_BASE}/discovery/results?date={latest_date}", headers=headers).json()
        if results:
            pick = results[0]
            print(f"Keys: {list(pick.keys())}")
            if "financials" in pick:
                print(f"Financials Keys: {list(pick['financials'].keys())}")
            if "technicals" in pick:
                print(f"Technicals Keys: {list(pick['technicals'].keys())}")
            
            # Print specific metrics from guide
            print(f"Paisa Score: {pick.get('paisa_score')}")
            print(f"Altman Z: {pick.get('financials', {}).get('altmanZScore')}")
            print(f"Expected Move: {pick.get('recommendation', {}).get('expected_move')}")
            print(f"RS: {pick.get('technicals', {}).get('rs')}")
            print(f"IV Rank: {pick.get('technicals', {}).get('volatility_rank')}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_discovery()

