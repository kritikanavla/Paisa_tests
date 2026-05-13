import json
import os

main_file = r'C:\\Users\\USER\.gemini\antigravity\scratch\Paisa tests\trade_data.json'
fidelity_file = r'C:\\Users\\USER\.gemini\antigravity\scratch\Paisa tests\scratch\fidelity_parsed.json'

with open(main_file, 'r') as f:
    main_trades = json.load(f)

with open(fidelity_file, 'r') as f:
    fidelity_trades = json.load(f)

# Append fidelity trades
main_trades.extend(fidelity_trades)

with open(main_file, 'w') as f:
    json.dump(main_trades, f, indent=4)

print(f"Successfully added {len(fidelity_trades)} trades from Fidelity CSV.")

