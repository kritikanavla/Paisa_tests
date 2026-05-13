import sys
import os
import asyncio

PAISA_SERVER_DIR = "C:\Users\USER/.gemini/antigravity/scratch/paisa/server"
sys.path.append(PAISA_SERVER_DIR)

from core.database import get_database, db_manager

async def main():
    try:
        await db_manager.connect()
        db = get_database()
        
        users = await db["users"].find().to_list(length=100)
        print("Users in DB:")
        for u in users:
            print(f" - {u.get('email')} (Role: {u.get('role')})")
            
        # Also check current session
        token = "ZyJ1aiWMTwXYLZpESbQJrPbVIqk9-3hkJA-PbfKM0zg"
        user = await db["users"].find_one({"session_token": token})
        if user:
            print(f"\nCURRENT SESSION USER: {user.get('email')}")
        else:
            print("\nTOKEN NOT FOUND IN DB")
            
        await db_manager.disconnect()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

