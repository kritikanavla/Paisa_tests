import requests
import json
import argparse
from datetime import datetime

# ==========================================
# Configuration
# ==========================================
API_BASE = "https://paisa.example.com/api"
SESSION_TOKEN = os.environ.get("PAISA_SESSION_TOKEN", "your_token_here")

class AgenticTrader:
    def __init__(self, persona="Trader"):
        self.headers = {"Authorization": f"Bearer {SESSION_TOKEN}"}
        self.persona = persona
        self.timestamp = datetime.now().strftime('%H:%M:%S')

    def log(self, message):
        print(f"[{self.timestamp}] [AGENT: {self.persona}] {message}")

    def run_daily_entries(self, dry_run=False):
        print("=" * 85)
        print(f"[{self.timestamp}] PAISA AGENTIC TRADER v1.0: Daily Entry Agent")
        print(f"Persona: {self.persona}")
        print("=" * 85)
        
        try:
            # 1. Fetch Latest Recommendations
            runs = requests.get(f"{API_BASE}/discovery/runs", headers=self.headers).json()
            if not runs:
                self.log("ERROR: No discovery runs found.")
                return
            
            latest_date = runs[0]['id']
            self.log(f"Fetching picks for {latest_date}...")
            picks = requests.get(f"{API_BASE}/discovery/results?date={latest_date}", headers=self.headers).json()
            
            if not picks:
                self.log("ERROR: No picks found for today.")
                return

            self.log(f"Analyzed {len(picks)} picks. Selecting high-conviction trades...")

            # 2. Diversified Selection Logic
            # Goal: One of each major strategy category
            categories = {
                "STOCK": "Classic Long Stock",
                "LEAPS": "ITM LEAPS",
                "SPREAD": "Bull Put Spread",
                "CSP": "Cash Secured Put"
            }
            
            selected_trades = {} # strategy_name -> pick
            
            # Sort picks by score descending
            sorted_picks = sorted(picks, key=lambda x: x.get("score", 0), reverse=True)
            
            for pick in sorted_picks:
                score = pick.get("score", 0)
                rec = pick.get("recommendation", {})
                action = (rec.get("action") or "").upper()
                
                # Check if any variant of BUY or SELL is in the action
                if score < 75 or not any(a in action for a in ["BUY", "SELL"]): 
                    continue # Conviction/Action threshold for "Trader" persona
                
                strategy = rec.get("strategy", "")
                ticker = pick.get("ticker")
                
                # Check for Stock
                if "STOCK" not in selected_trades and strategy == "Classic Long Stock":
                    selected_trades["STOCK"] = pick
                    self.log(f"Selected STOCK: {ticker} (Score: {score})")
                
                # Check for Options/Leaps
                if "LEAPS" not in selected_trades and "LEAP" in strategy.upper():
                    selected_trades["LEAPS"] = pick
                    self.log(f"Selected LEAP: {ticker} (Score: {score})")
                
                # Check for Spreads
                if "SPREAD" not in selected_trades and "SPREAD" in strategy.upper():
                    selected_trades["SPREAD"] = pick
                    self.log(f"Selected SPREAD: {ticker} (Score: {score})")
                
                # Check for CSP
                if "CSP" not in selected_trades and any(s in strategy.upper() for s in ["CSP", "NAKED PUT"]):
                    selected_trades["CSP"] = pick
                    self.log(f"Selected CSP: {ticker} (Score: {score})")

            if not selected_trades:
                self.log("No trades met the conviction threshold today.")
                return

            # 3. Execution Phase
            self.log(f"Preparing to execute {len(selected_trades)} trades...")
            for cat, pick in selected_trades.items():
                self.execute_trade(pick, dry_run)

        except Exception as e:
            self.log(f"FATAL ERROR: {str(e)}")

    def execute_trade(self, pick, dry_run=False):
        ticker = pick.get("ticker")
        rec = pick.get("recommendation", {})
        strategy = rec.get("strategy")
        trade_type = rec.get("option_type") or "STOCK"
        price = pick.get("price")
        
        # Build Trade Payload
        trade_payload = {
            "ticker": ticker,
            "symbol": ticker if trade_type == "STOCK" else pick.get("leaps", {}).get("contract", ticker),
            "entry_price": price if trade_type == "STOCK" else pick.get("leaps", {}).get("premium", 1.0),
            "status": "OPEN",
            "trade_type": trade_type,
            "strategy": strategy,
            "strategy_type": strategy,
            "quantity": 100 if trade_type == "STOCK" else 1,
            "action": rec.get("action", "BUY"),
            "is_robo": True,
            "recorded_at": datetime.now().isoformat()
        }
        
        # If it's a spread, handle legs
        # Note: In a real system, we'd need leg data. For now, we use the simplified model.
        
        if dry_run:
            self.log(f"[DRY RUN] Would enter {strategy} on {ticker} at ${trade_payload['entry_price']}")
        else:
            self.log(f"Entering {strategy} on {ticker}...")
            resp = requests.post(f"{API_BASE}/trades/save", headers=self.headers, json=trade_payload)
            if resp.status_code == 200:
                result = resp.json()
                if result.get("status") == "success":
                    self.log(f"SUCCESS: Trade {result.get('trade_id')} recorded for {ticker}.")
                else:
                    self.log(f"FAILED: {result.get('message')}")
            else:
                self.log(f"API ERROR: {resp.status_code}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Paisa Agentic Trader CLI")
    parser.add_argument("--dry-run", action="store_true", help="Do not execute trades")
    args = parser.parse_args()
    
    trader = AgenticTrader()
    trader.run_daily_entries(dry_run=args.dry_run)

