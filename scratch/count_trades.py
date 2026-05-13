import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load env from server directory
load_dotenv(dotenv_path="C:\Users\USER/.gemini/antigravity/scratch/paisa/server/.env")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "paisa_db"

async def count_trades():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    user_email = "test_user_a@example.com"
    
    print(f"--- Trade counts for {user_email} ---")
    
    pipeline = [
        {"$match": {"user_id": user_email, "status": "OPEN"}},
        {"$group": {"_id": "$ticker", "count": {"$sum": 1}, "total_qty": {"$sum": "$quantity"}}}
    ]
    
    cursor = db["trades"].aggregate(pipeline)
    async for doc in cursor:
        print(f"Ticker: {doc['_id']}, Trades: {doc['count']}, Total Qty: {doc['total_qty']}")

    client.close()

if __name__ == "__main__":
    asyncio.run(count_trades())

