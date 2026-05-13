import sys
import os
import json
import time
from datetime import datetime

# Add current dir to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from planner_agent import PlannerAgent
from execution_agent import ExecutionAgent
from auditor_agent import AuditorAgent

class QAOrchestrator:
    """
    The Master Orchestrator: Coordinates the 3-agent squad to execute 
    the full testing lifecycle.
    """
    def __init__(self, api_base, token, cloud_id=None):
        self.api_base = api_base
        self.token = token
        self.cloud_id = cloud_id
        
        self.planner = PlannerAgent()
        self.executor = ExecutionAgent()
        self.auditor = AuditorAgent(api_base, token, cloud_id)

    def log(self, message):
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"\n[ORCHESTRATOR] [{timestamp}] {message}")
        print("="*80)

    def run_cycle(self):
        self.log("Starting QA Lifecycle Cycle...")

        # Step 1: Planning
        trades = self.planner.generate_adversarial_trades(5)
        plan_file = self.planner.save_plan(trades)

        # Step 2: Execution & Injection
        # Note: In a real run, the executor would call the population script
        self.log(f"Phase 2: Injecting adversarial trades from {plan_file}...")
        # (Placeholder for actual injection logic)
        
        # Step 3: UI Testing
        ui_results = self.executor.run_tests()
        if ui_results["status"] == "needs_healing":
            self.log(f"Self-Healing required for: {ui_results['candidates']}")
            # Trigger healer logic here

        # Step 4: Logic Audit
        self.log("Phase 4: Mathematical Risk Engine Audit...")
        summary = self.auditor.fetch_portfolio_summary()
        mismatches = self.auditor.audit_risk_metrics(summary)
        
        if mismatches:
            self.log(f"ALERT: Detected {len(mismatches)} logic mismatches!")
            for m in mismatches:
                print(f"  - {m['metric']}: {m['auditor']} (Auditor) vs {m['system']} (System) [{m['severity']}]")
            
            # Step 5: Incident Reporting (Return for MCP tool usage)
            return {
                "status": "complete_with_errors",
                "mismatches": mismatches,
                "ui_status": ui_results["status"]
            }

        self.log("QA Cycle Complete. System stable.")
        return {"status": "success", "ui_status": ui_results["status"]}

if __name__ == "__main__":
    API_BASE = "https://paisa.example.com/api"
    TOKEN = "ZyJ1aiWMTwXYLZpESbQJrPbVIqk9-3hkJA-PbfKM0zg"
    
    orchestrator = QAOrchestrator(API_BASE, TOKEN)
    final_report = orchestrator.run_cycle()
    
    print("\nFINAL REPORT:")
    print(json.dumps(final_report, indent=2))

