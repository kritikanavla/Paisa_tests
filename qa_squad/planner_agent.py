import json
import random
from datetime import datetime, timedelta

class PlannerAgent:
    """
    The Planner Agent: Responsible for generating dynamic test scenarios 
    and adversarial datasets to stress-test the system.
    """
    def __init__(self):
        self.tickers = ["AAPL", "NVDA", "TSLA", "AMD", "MSFT", "GOOGL", "AMZN"]
        self.strategies = ["Core: ZEBRA", "Bull Call Spread", "Iron Condor", "Momentum Play"]

    def log(self, message):
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[PLANNER] [{timestamp}] {message}")

    def generate_adversarial_trades(self, count=5):
        """
        Generates edge-case trade data to stress the Risk Engine.
        """
        self.log(f"Generating {count} adversarial test cases...")
        trades = []
        
        # Scenario 1: Extreme Quantity
        trades.append({
            "ticker": "AAPL",
            "quantity": 1000000,
            "price": 180.0,
            "date": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
            "strategy_type": "Stress Test: Whale"
        })
        
        # Scenario 2: Deep ITM Short Option (Testing Delta/Sign handling)
        trades.append({
            "ticker": "NVDA",
            "quantity": -10,
            "price": 500.0,
            "trade_type": "OPTION",
            "expiry": "2026-12-15",
            "date": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
            "strategy_type": "Stress Test: Inverse Delta"
        })

        # Scenario 3: Highly Volatile Pennystock (High Beta simulation)
        trades.append({
            "ticker": "GME",
            "quantity": 5000,
            "price": 15.0,
            "date": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
            "strategy_type": "Stress Test: Beta Spike"
        })

        # Fill the rest with random data
        for _ in range(count - 3):
            ticker = random.choice(self.tickers)
            trades.append({
                "ticker": ticker,
                "quantity": random.randint(1, 500),
                "price": random.uniform(50, 500),
                "date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
                "strategy_type": random.choice(self.strategies)
            })

        return trades

    def save_plan(self, trades, filename="adversarial_plan.json"):
        with open(filename, "w") as f:
            json.dump(trades, f, indent=2)
        self.log(f"Test plan saved to {filename}")
        return filename

if __name__ == "__main__":
    planner = PlannerAgent()
    trades = planner.generate_adversarial_trades(10)
    planner.save_plan(trades)
