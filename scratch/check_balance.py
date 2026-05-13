import requests
API_BASE = "https://paisa.example.com/api"
SESSION_TOKEN = "JoZ--gQaSvmgndFUFwtoaVLGVitbhCbWjguWroS1VcM"
HEADERS = {"Authorization": f"Bearer {SESSION_TOKEN}"}

def check_balance():
    summary = requests.get(f"{API_BASE}/portfolio/summary", headers=HEADERS).json()
    print(f"Current Buying Power: ${summary.get('buying_power'):,.2f}")

if __name__ == "__main__":
    check_balance()

