import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def setup_onboarding_test():
    client = AsyncIOMotorClient("mongodb://localhost:27017/")
    db = client['paisa_db']
    
    # 1. Register a fresh user if not exists
    email = "onboarding_test@example.com"
    password_hash = b'$2b$12$K7v19.FqH2kL8fQ.Q1lG.eUj0G0z7H9w8kL8fQ.Q1lG.eUj0G0z7H' # "Password123!"
    
    user = await db['users'].find_one({"email": email})
    if not user:
        await db['users'].insert_one({
            "email": email,
            "password_hash": password_hash,
            "is_verified": True,
            "is_approved": True,
            "persona": None,
            "created_at": "2024-01-01"
        })
        print(f"Created user: {email}")
    else:
        # Reset persona to None
        await db['users'].update_one(
            {"email": email},
            {"$set": {"persona": None, "is_verified": True, "is_approved": True}}
        )
        print(f"Reset user: {email}")
        
    client.close()

if __name__ == "__main__":
    asyncio.run(setup_onboarding_test())
