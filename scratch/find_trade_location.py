import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load env from server directory
load_dotenv(dotenv_path="C:\Users\USER/.gemini/antigravity/scratch/paisa/server/.env")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "paisa_db"

async def find_trade_collection():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    user_email = "test_user_a@example.com"
    
    print(f"--- Searching all collections for {user_email} ---")
    
    collections = ["trades", "external_portfolios", "portfolio_state", "external_portfolio_state"]
    
    for coll in collections:
        count = await db[coll].count_documents({"user_id": user_email})
        print(f"Collection '{coll}': {count} documents.")
        if count > 0:
            doc = await db[coll].find_one({"user_id": user_email})
            if "trades" in doc:
                 print(f"  -> Found {len(doc['trades'])} trades inside document.")
            elif "details" in doc.get("beta_data_full", {}):
                 print(f"  -> Found {len(doc['beta_data_full']['details'])} entries in risk details.")

    client.close()

if __name__ == "__main__":
    asyncio.run(find_trade_collection())

