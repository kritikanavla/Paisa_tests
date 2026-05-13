import requests
import json

API_BASE = "https://paisa.example.com/api"
SESSION_TOKEN = "ZyJ1aiWMTwXYLZpESbQJrPbVIqk9-3hkJA-PbfKM0zg"

def inspect_summary():
    headers = {"Authorization": f"Bearer {SESSION_TOKEN}"}
    try:
        resp = requests.get(f"{API_BASE}/portfolio/summary", headers=headers)
        print(f"Status: {resp.status_code}")
        data = resp.json()
        # Remove large items to see structure
        if "risk_details" in data:
            print(f"Found {len(data['risk_details'])} items in risk_details")
            # data['risk_details'] = {k: "..." for k in list(data['risk_details'].keys())[:2]}
        
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_summary()

