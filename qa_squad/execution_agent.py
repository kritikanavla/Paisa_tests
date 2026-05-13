import subprocess
import os
import json
from datetime import datetime

class ExecutionAgent:
    """
    The Execution Agent: Responsible for running Playwright tests and 
    handling self-healing when UI selectors fail.
    """
    def __init__(self, test_dir="tests"):
        self.test_dir = test_dir

    def log(self, message):
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[EXECUTION] [{timestamp}] {message}")

    def run_tests(self, filter=None):
        self.log(f"Running UI Test Suite in {self.test_dir}...")
        
        cmd = ["py", "-m", "pytest", self.test_dir, "--json-report", "--json-report-file=report.json"]
        if filter:
            cmd.extend(["-k", filter])
            
        try:
            # Running with 'py' on Windows if needed, otherwise 'pytest'
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.log("Test suite execution complete.")
            
            # Check for failures that might need healing
            if result.returncode != 0:
                self.log("Failures detected. Analyzing for self-healing opportunities...")
                return self.analyze_failures()
            
            return {"status": "success", "message": "All tests passed."}
            
        except Exception as e:
            self.log(f"Fatal error during test execution: {e}")
            return {"status": "error", "message": str(e)}

    def analyze_failures(self):
        """
        The Healer Logic: Analyzes report.json to identify if a failure 
        is due to a missing locator.
        """
        if not os.path.exists("report.json"):
             return {"status": "fail", "message": "Tests failed, no report found."}
             
        with open("report.json", "r") as f:
            report = json.load(f)
            
        failures = [test for test in report.get("tests", []) if test.get("outcome") == "failed"]
        self.log(f"Found {len(failures)} test failures.")
        
        # Simple heuristic for healing: look for TimeoutError or NoSuchElement
        healing_candidates = []
        for fail in failures:
            longrepr = fail.get("call", {}).get("longrepr", "")
            if "TimeoutError" in longrepr or "waiting for locator" in longrepr:
                healing_candidates.append(fail["nodeid"])
        
        if healing_candidates:
            self.log(f"Identified {len(healing_candidates)} candidates for AI Healing.")
            return {"status": "needs_healing", "candidates": healing_candidates}
            
        return {"status": "fail", "failures": failures}

if __name__ == "__main__":
    runner = ExecutionAgent()
    results = runner.run_tests()
    print(json.dumps(results, indent=2))
