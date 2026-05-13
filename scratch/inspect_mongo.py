import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load env from server directory
load_dotenv(dotenv_path="C:\Users\USER/.gemini/antigravity/scratch/paisa/server/.env")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "paisa_db"

async def check_trades():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    user_email = "test_user_a@example.com"
    
    print(f"--- Checking trades for {user_email} ---")
    trades_cursor = db["trades"].find({"user_id": user_email, "status": "OPEN"})
    trades = await trades_cursor.to_list(length=100)
    
    print(f"Found {len(trades)} open trades.")
    for t in trades:
        print(f"Ticker: {t.get('ticker')}, Qty: {t.get('quantity')}, Price: {t.get('entry_price')}")

    print("\n--- Checking Risk State ---")
    state = await db["portfolio_states"].find_one({"user_id": user_email, "target": "real"})
    if state:
        print(f"Last Synced: {state.get('last_synced')}")
        print(f"Net Beta Delta: {state.get('net_beta_delta')}")
        print(f"Total Market Value: {state.get('total_market_value')}")
    else:
        print("No risk state found.")

    client.close()

if __name__ == "__main__":
    asyncio.run(check_trades())

