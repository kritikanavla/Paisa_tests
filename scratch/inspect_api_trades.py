import requests
import json

API_BASE = "https://paisa.example.com/api"
SESSION_TOKEN = "JoZ--gQaSvmgndFUFwtoaVLGVitbhCbWjguWroS1VcM"

def inspect_active_trades():
    headers = {"Authorization": f"Bearer {SESSION_TOKEN}"}
    resp = requests.get(f"{API_BASE}/trades/active", headers=headers)
    trades = resp.json()
    
    if trades:
        print(f"--- First Trade Detail ({trades[0].get('ticker')}) ---")
        print(json.dumps(trades[0], indent=2))
    else:
        print("No active trades found.")

if __name__ == "__main__":
    inspect_active_trades()

