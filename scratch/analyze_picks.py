import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check():
    client = AsyncIOMotorClient('mongodb://localhost:27017/')
    db = client['paisa_db']
    
    doc = await db["daily_picks"].find_one(sort=[("date", -1)])
    if doc:
        print(f"Date: {doc.get('date')}")
        picks = doc.get("picks", [])
        print(f"Total Picks: {len(picks)}")
        
        strategies = set()
        for p in picks:
            strat = p.get("recommendation", {}).get("strategy") or p.get("strategy")
            if strat: strategies.add(strat)
        print(f"Strategies found: {list(strategies)}")
    else:
        print("No daily picks found.")

    client.close()

if __name__ == "__main__":
    asyncio.run(check())
