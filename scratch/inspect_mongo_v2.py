import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import json

# Load env from server directory
load_dotenv(dotenv_path="C:\Users\USER/.gemini/antigravity/scratch/paisa/server/.env")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "paisa_db"

async def check_trades():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    user_email = "test_user_a@example.com"
    
    print(f"--- Checking trades for {user_email} ---")
    # Ticker might be under 'ticker' or 'Ticker' depending on the importer
    trades_cursor = db["trades"].find({"user_id": user_email, "status": "OPEN"})
    trades = await trades_cursor.to_list(length=100)
    
    print(f"Found {len(trades)} open trades.")
    for t in trades:
        print(f"Ticker: {t.get('ticker') or t.get('Ticker')}, Qty: {t.get('quantity') or t.get('Quantity')}, Entry: {t.get('entry_price') or t.get('Entry')}")

    print("\n--- Checking Risk State ---")
    # Corrected collection name: portfolio_state (singular)
    state = await db["portfolio_state"].find_one({"user_id": user_email})
    if state:
        # Don't print the whole thing, just key metrics
        print(f"Last Synced: {state.get('last_synced')}")
        print(f"Net Beta Delta: {state.get('net_beta_delta')}")
        print(f"Total Market Value: {state.get('total_market_value')}")
        print(f"Sync Status: {state.get('sync_status')}")
        
        # Check details for MSFT or something
        details = state.get("beta_data_full", {}).get("details", {})
        if details:
            print(f"Number of symbols in risk details: {len(details)}")
            # Show one example
            first_ticker = list(details.keys())[0]
            print(f"Example ({first_ticker}): {json.dumps(details[first_ticker], indent=2)}")
    else:
        print("No risk state found.")

    client.close()

if __name__ == "__main__":
    asyncio.run(check_trades())

