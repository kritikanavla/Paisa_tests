from pymongo import MongoClient
import os
from dotenv import load_dotenv
import json

# Load env from server directory
load_dotenv(dotenv_path="C:\Users\USER/.gemini/antigravity/scratch/paisa/server/.env")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "paisa_db"

def inspect_raw_trade():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    
    user_email = "test_user_a@example.com"
    
    print(f"--- Raw Trade Data (Blocking) for {user_email} ---")
    trade = db["trades"].find_one({"user_id": user_email, "ticker": "INTC"})
    if trade:
        # Remove ObjectId for printing
        if "_id" in trade: trade["_id"] = str(trade["_id"])
        print(json.dumps(trade, indent=2))
    else:
        print("No INTC trade found.")

    client.close()

if __name__ == "__main__":
    inspect_raw_trade()

