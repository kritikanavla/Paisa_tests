import requests
import json

API_BASE = "https://paisa.example.com/api"
TOKEN = "ZyJ1aiWMTwXYLZpESbQJrPbVIqk9-3hkJA-PbfKM0zg"

headers = {"Authorization": f"Bearer {TOKEN}"}

try:
    response = requests.get(f"{API_BASE}/portfolio/summary", headers=headers)
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")

