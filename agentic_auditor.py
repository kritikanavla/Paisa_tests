import requests
import json
import argparse
from datetime import datetime

# ==========================================
# Configuration
# ==========================================
API_BASE = "https://paisa.example.com/api"
SESSION_TOKEN = os.environ.get("PAISA_SESSION_TOKEN", "your_token_here")

class AgenticAuditor:
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {SESSION_TOKEN}"}
        self.timestamp = datetime.now().strftime('%H:%M:%S')

    def log(self, message):
        print(f"[{self.timestamp}] {message}")

    def run_full_audit(self, mode="auto"):
        print("=" * 85)
        print(f"[{self.timestamp}] PAISA AGENTIC AUDITOR v6.0: Unified Verification Engine")
        print("=" * 85)
        
        try:
            # 0. Trigger Sync (to ensure latest trades are reflected)
            self.log("Triggering Portfolio Sync...")
            requests.post(f"{API_BASE}/portfolio/sync", headers=self.headers)
            # Small delay for sync to start/complete
            import time
            time.sleep(2)

            # 1. Fetch System State
            summary = requests.get(f"{API_BASE}/portfolio/summary", headers=self.headers).json()
            active_trades = summary.get("active_trades_count", 0)
            sync_status = summary.get("sync_status", "pending")
            
            self.log(f"Portfolio Sync Status: {sync_status} | Active Trades: {active_trades}")
            
            # 2. Decision Logic
            do_portfolio = mode in ["auto", "portfolio"]
            do_discovery = mode in ["auto", "discovery"]
            
            if do_portfolio:
                self.audit_portfolio_risk(summary)
            
            if do_discovery:
                self.audit_discovery_metrics()
                
            print("\n" + "=" * 85)
            print(f"[{self.timestamp}] Audit Session Complete.")
            print("=" * 85)

        except Exception as e:
            print(f"\n[FATAL] Audit System Failure: {str(e)}")

    def audit_portfolio_risk(self, summary):
        print("\n--- [MODULE: PORTFOLIO RISK & STRESS] ---")
        risk_details = summary.get("risk_details", {})
        total_cap = summary.get("total_capital", 100000.0)
        
        spy_price = summary.get("beta_data_full", {}).get("spy_price")
        if not spy_price:
             spy_price = risk_details.get("SPY", {}).get("price", 500.0)
        
        self.log(f"System State: {summary.get('active_trades_count')} Active Trades | Capital: ${total_cap:,.2f}")
        
        if not risk_details:
            print("INFO: No active trades found. Portfolio risk audit skipped.")
            return

        exposure_sum = 0.0
        pnl_errors = []
        
        print(f"{'Symbol':<15} | {'Qty':<6} | {'Delta':<8} | {'Beta':<6} | {'Exposure ($)':<15}")
        print("-" * 80)
        
        for symbol, data in risk_details.items():
            if symbol == "SPY": continue
            
            qty = float(data.get("quantity", 0))
            delta = float(data.get("delta", 1.0))
            beta = float(data.get("beta", 1.0))
            price = float(data.get("price", 0))
            entry = float(data.get("entry_price", 0))
            actual_pnl = float(data.get("pnl_pct", 0))
            multiplier = 100 if data.get("trade_type") == "OPTION" else 1
            
            # --- P&L Audit (Strategy Aware) ---
            direction = 1 if qty >= 0 else -1
            if entry != 0:
                expected_pnl = ((price - entry) / entry) * direction
                if abs(expected_pnl - actual_pnl) > 0.01:
                    pnl_errors.append(f"{symbol}: Exp {expected_pnl:.1%} vs Sys {actual_pnl:.1%}")

            # --- Exposure Audit ---
            # SYSTEM BEHAVIOR: 
            # - The Risk Engine is reporting TOTAL AGGREGATED delta (Delta * Qty * Multiplier)
            #   in the 'delta' field of 'risk_details'.
            
            # Formula: Total Delta * Beta * (Price / SPY_Price)
            pos_exposure_spy = (delta) * beta * (price / spy_price)
            exposure_sum += pos_exposure_spy
            
            print(f"{symbol:<15} | {qty:<6.1f} | {delta:<8.2f} | {beta:<6.2f} | ${pos_exposure_spy * spy_price:,.2f}")

        # Final Portfolio Math
        audit_bwe = exposure_sum * spy_price
        sys_bwe = summary.get('net_beta_delta', 0) * spy_price
        sys_vega = summary.get("vega_impact", 0)
        
        # Stress Test: -10% Market Drop
        audit_crash_impact = (audit_bwe * -0.10) + sys_vega
        audit_drawdown = (audit_crash_impact / total_cap) * 100
        
        print("-" * 80)
        print(f"{'METRIC':<25} | {'AUDITOR':<15} | {'SYSTEM':<15} | {'STATUS'}")
        print("-" * 80)
        
        def status(a, s, tol=1000): return "OK" if abs(a - s) < tol else "MISMATCH"

        print(f"{'Beta-Weighted Exposure':<25} | ${audit_bwe:<14,.2f} | ${sys_bwe:<14,.2f} | {status(audit_bwe, sys_bwe)}")
        print(f"{'Projected Dollar Impact':<25} | ${audit_crash_impact:<14,.2f} | ${summary.get('crash_projection',0):<14,.2f} | {status(audit_crash_impact, summary.get('crash_projection',0))}")
        print(f"{'Projected Drawdown (%)':<25} | {audit_drawdown:<14.2f}% | {summary.get('crash_drawdown_ref',0):<14.2f}% | {status(audit_drawdown, summary.get('crash_drawdown_ref',0), 0.5)}")

    def audit_discovery_metrics(self):
        print("\n--- [MODULE: DISCOVERY & STATIC METRICS] ---")
        try:
            runs = requests.get(f"{API_BASE}/discovery/runs", headers=self.headers).json()
            if not runs:
                print("WARNING: No discovery runs available for audit.")
                return
            
            latest_date = runs[0]['id']
            results = requests.get(f"{API_BASE}/discovery/results?date={latest_date}", headers=self.headers).json()
            
            if not results:
                print(f"WARNING: No picks found for {latest_date}.")
                return

            sample = results[0]
            print(f"Sample Ticker: {sample.get('ticker')} (Universe: {len(results)} stocks)")
            print("-" * 80)
            print(f"{'METRIC':<25} | {'FIELD':<20} | {'VALUE':<15} | {'STATUS'}")
            print("-" * 80)
            
            metrics = [
                ("Paisa Score", "score", sample.get("score")),
                ("Expected Move (7d)", "expected_move_7d", sample.get("expected_move_7d")),
                ("IV Rank", "iv_rank", sample.get("iv_rank")),
                ("Relative Strength", "rs_score", sample.get("rs_score")),
                ("Confidence Score", "confidence_score", sample.get("confidence_score"))
            ]
            
            for name, field, val in metrics:
                s = "OK" if val is not None else "MISSING"
                print(f"{name:<25} | {field:<20} | {str(val):<15} | {s}")
            
            print("-" * 80)
            print(f"Data Status: {sample.get('data_status', 'Unknown')}")
            missing = sample.get("missing_metrics", [])
            if missing:
                print(f"Notes: The following sub-metrics were missing: {', '.join(missing)}")

        except Exception as e:
            print(f"Discovery Audit Error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Paisa Agentic Auditor Unified CLI")
    parser.add_argument("--mode", choices=["auto", "portfolio", "discovery"], default="auto", help="Audit mode")
    args = parser.parse_args()
    
    auditor = AgenticAuditor()
    auditor.run_full_audit(mode=args.mode)

