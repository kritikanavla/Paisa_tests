import sys
import os
import asyncio

PAISA_SERVER_DIR = "C:\Users\USER/.gemini/antigravity/scratch/paisa/server"
sys.path.append(PAISA_SERVER_DIR)

from core.database import get_database, db_manager

async def check_user_trades():
    USER_ID = "test_user_a@example.com"
    try:
        await db_manager.connect()
        db = get_database()
        
        print(f"Checking trades for {USER_ID}...")
        
        # 1. Check Real Portfolio
        open_trades = await db["trades"].find({"user_id": USER_ID, "status": "OPEN"}).to_list(length=100)
        print(f"Open Trades: {len(open_trades)}")
        for t in open_trades:
            print(f" - {t.get('ticker')} (ID: {t.get('id')})")
            
        # 2. Check External Lab
        ext_trades = await db["external_portfolios"].find({"user_id": USER_ID}).to_list(length=100)
        print(f"External Lab Trades: {len(ext_trades)}")
        
        await db_manager.disconnect()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_user_trades())

