from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Manual URI for local verification
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "paisa_db"
USER_EMAIL = "test_user_a@example.com"

def check_reset_status():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        db = client[DB_NAME]
        
        # 1. Count Trades
        trades_count = db["trades"].count_documents({"user_id": USER_EMAIL})
        
        # 2. Check Balance in user_settings
        settings = db["user_settings"].find_one({"key": "user_config", "user_id": USER_EMAIL})
        balance = settings.get("buying_power") if settings else "NOT FOUND"
        
        print(f"Audit Result for {USER_EMAIL}:")
        print(f"  Trades Count: {trades_count}")
        print(f"  Buying Power: ${balance}")
        
        client.close()
    except Exception as e:
        print(f"Audit Failed: {e}")

if __name__ == "__main__":
    check_reset_status()
