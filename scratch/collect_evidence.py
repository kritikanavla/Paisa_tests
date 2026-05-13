import requests
headers = {'Authorization': 'Bearer ZyJ1aiWMTwXYLZpESbQJrPbVIqk9-3hkJA-PbfKM0zg'}
r = requests.get('https://paisa.example.com/api/portfolio/summary', headers=headers).json()

net_beta_delta = r.get("net_beta_delta", 0)
spy_equiv = r.get("spy_equivalent_shares", 0)
spy_price = r.get("beta_data_full", {}).get("spy_price", 500)
exposure = net_beta_delta * spy_price

print(f"--- [ BUG EVIDENCE: EXTREME VALUES ] ---")
print(f"net_beta_delta: {net_beta_delta}")
print(f"spy_equivalent_shares: {spy_equiv}")
print(f"Calculated Exposure: ${exposure:,.2f}")
print(f"SPY Benchmark Price: ${spy_price}")
print(f"----------------------------------------")

