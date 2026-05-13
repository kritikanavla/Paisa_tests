import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os

async def find_admin():
    MONGO_URI = "mongodb://localhost:27017/"
    client = AsyncIOMotorClient(MONGO_URI)
    db = client['paisa_db']
    
    # Find a super admin
    admin = await db['users'].find_one({"role": "super_admin"})
    if admin:
        print(f"ADMIN_EMAIL: {admin['email']}")
    else:
        print("No super admin found.")
        
    client.close()

if __name__ == "__main__":
    asyncio.run(find_admin())
