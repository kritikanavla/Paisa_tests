import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone, timedelta

async def check():
    client = AsyncIOMotorClient('mongodb://localhost:27017/')
    db = client['paisa_db']
    
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    yesterday_str = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
    
    print(f"Checking daily_picks for {date_str} and {yesterday_str}...")
    
    doc = await db["daily_picks"].find_one({"date": date_str})
    if doc:
        print(f"Found {len(doc.get('picks', []))} picks for today.")
    else:
        print("No picks found for today.")
        doc = await db["daily_picks"].find_one({"date": yesterday_str})
        if doc:
            print(f"Found {len(doc.get('picks', []))} picks for yesterday.")
        else:
            print("No picks found for yesterday.")

    client.close()

if __name__ == "__main__":
    asyncio.run(check())
