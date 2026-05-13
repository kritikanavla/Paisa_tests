import requests
import json
from datetime import datetime

class AuditorAgent:
    """
    The Auditor Agent: Responsible for mathematical verification of the Risk Engine.
    It compares system-reported values against independent audit calculations.
    """
    def __init__(self, api_base, session_token, cloud_id=None):
        self.api_base = api_base
        self.headers = {"Authorization": f"Bearer {session_token}"}
        self.cloud_id = cloud_id # For Jira reporting

    def log(self, message):
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[AUDITOR] [{timestamp}] {message}")

    def fetch_portfolio_summary(self):
        self.log("Fetching Portfolio Summary...")
        try:
            response = requests.get(f"{self.api_base}/portfolio/summary", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Error fetching summary: {e}")
            return None

    def audit_risk_metrics(self, summary):
        if not summary:
            return None

        self.log("Starting Mathematical Audit...")
        risk_details = summary.get("risk_details", {})
        spy_price = summary.get("beta_data_full", {}).get("spy_price", 500.0)
        
        exposure_sum = 0.0
        mismatches = []

        for symbol, data in risk_details.items():
            if symbol == "SPY": continue
            
            delta = float(data.get("delta", 0))
            beta = float(data.get("beta", 1.0))
            price = float(data.get("price", 0))
            
            # Auditor Calculation: Total Delta * Beta * (Price / SPY_Price)
            pos_exposure_spy = (delta) * beta * (price / spy_price)
            exposure_sum += pos_exposure_spy

        audit_bwe = exposure_sum * spy_price
        sys_bwe = summary.get('net_beta_delta', 0) * spy_price
        
        # Check for 1,000x inflation or significant mismatch (> 1% tolerance)
        if abs(audit_bwe - sys_bwe) > (abs(audit_bwe) * 0.01 + 1000):
            mismatches.append({
                "metric": "Beta-Weighted Exposure",
                "auditor": f"${audit_bwe:,.2f}",
                "system": f"${sys_bwe:,.2f}",
                "severity": "CRITICAL" if abs(sys_bwe / (audit_bwe or 1)) > 10 else "MEDIUM"
            })

        # Check Stress Projections
        sys_crash = summary.get('crash_projection', 0)
        if abs(sys_crash) < 0.01 and abs(audit_bwe) > 1000:
             mismatches.append({
                "metric": "Projected Dollar Impact",
                "auditor": f"${(audit_bwe * -0.10):,.2f}",
                "system": "$0.00",
                "severity": "MEDIUM",
                "note": "System reports zero risk despite high exposure."
            })

        # 3. Greek Sensitivity Audit (PAISA-7 Verification)
        greek_mismatches = self.audit_greek_sensitivity(risk_details)
        mismatches.extend(greek_mismatches)

        return mismatches

    def audit_greek_sensitivity(self, risk_details):
        self.log("Auditing Greek Sensitivity (IV Stalling)...")
        iv_values = []
        for symbol, data in risk_details.items():
            iv = data.get("iv") or data.get("implied_volatility")
            if iv: iv_values.append(float(iv))
        
        mismatches = []
        # Detection: If > 50% of positions have exactly 0.3 IV, it's a proxy stall
        if iv_values:
            proxies = [v for v in iv_values if abs(v - 0.3) < 0.0001]
            if len(proxies) / len(iv_values) > 0.5:
                mismatches.append({
                    "metric": "Greek Sensitivity",
                    "auditor": "Live Market IV",
                    "system": "Static 30% Proxy (Detected)",
                    "severity": "HIGH",
                    "note": "Risk Engine is stalling on flat IV proxies. Delta precision compromised."
                })
        return mismatches

    def report_to_jira(self, mismatches):
        """
        Note: This is a placeholder for the Orchestrator to call 
        the Atlassian MCP tool 'createJiraIssue'.
        """
        if not mismatches:
            return "No mismatches to report."
        
        self.log(f"Detected {len(mismatches)} mismatches. Preparing Jira reports...")
        return mismatches # Return to Orchestrator for tool calling

if __name__ == "__main__":
    # Quick standalone test with existing credentials
    API_BASE = "https://paisa.example.com/api"
    TOKEN = "ZyJ1aiWMTwXYLZpESbQJrPbVIqk9-3hkJA-PbfKM0zg"
    
    auditor = AuditorAgent(API_BASE, TOKEN)
    summary = auditor.fetch_portfolio_summary()
    results = auditor.audit_risk_metrics(summary)
    print(json.dumps(results, indent=2))

