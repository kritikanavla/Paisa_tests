import json
import requests

EMAIL = "test_user_a@example.com"
PASSWORD = "Password123!"
BASE_URL = "https://paisa.example.com"

def verify_api():
    # Login
    print(f"Logging into {BASE_URL}...")
    login_url = f"{BASE_URL}/api/auth/login"
    login_res = requests.post(login_url, json={"email": EMAIL, "password": PASSWORD})
    
    if login_res.status_code != 200:
        print(f"Login failed: {login_res.text}")
        return
    
    token = login_res.json().get("token")
    print("Logged in successfully.")
    
    # Check active trades
    print("Fetching active trades...")
    trades_url = f"{BASE_URL}/api/trades/active"
    trades_res = requests.get(trades_url, headers={"Authorization": f"Bearer {token}"})
    
    if trades_res.status_code != 200:
        print(f"Failed to fetch trades: {trades_res.text}")
        return
    
    trades = trades_res.json()
    print(f"Number of active trades returned by API: {len(trades)}")
    
    if len(trades) > 0:
        print("Sample tickers in API:")
        for t in trades[:5]:
            print(f"  - {t.get('ticker')}")
    else:
        print("API returned 0 active trades.")
        
    # Check if there are any trades at all (even if not active)
    # We don't have a direct 'all trades' endpoint in the hook, but let's see
    
if __name__ == "__main__":
    verify_api()

