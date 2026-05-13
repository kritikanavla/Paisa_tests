import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check():
    client = AsyncIOMotorClient('mongodb://localhost:27017/')
    db = client['paisa_db']
    
    trade = await db["trades"].find_one({"ticker": "CAT", "user_id": "test@example.com"})
    import json
    from bson import json_util
    print(json.dumps(trade, indent=2, default=json_util.default))

    client.close()

if __name__ == "__main__":
    asyncio.run(check())
