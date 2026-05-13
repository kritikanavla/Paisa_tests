import motor.motor_asyncio
import asyncio

async def test_mongo_multi():
    uris = [
        "mongodb://localhost:27017/",
        "mongodb://127.0.0.1:27017/",
        "mongodb://0.0.0.0:27017/"
    ]
    
    for uri in uris:
        print(f"Trying {uri}...")
        try:
            client = motor.motor_asyncio.AsyncIOMotorClient(uri, serverSelectionTimeoutMS=2000)
            await client.admin.command('ping')
            print(f"SUCCESS: {uri} is UP")
            return uri
        except Exception as e:
            print(f"FAILED: {uri} - {e}")
    return None

if __name__ == "__main__":
    asyncio.run(test_mongo_multi())
