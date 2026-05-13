import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check():
    client = AsyncIOMotorClient('mongodb://localhost:27017/')
    db = client['paisa_db']
    
    print("--- Users ---")
    users = await db['users'].find().to_list(10)
    for u in users:
        print(f"Email: {u.get('email')}")
        
    print("\n--- Portfolio States ---")
    states = await db['portfolio_states'].find().to_list(10)
    for s in states:
        print(f"User: {s.get('user_id')}, Delta: {s.get('net_beta_delta')}, Health: {s.get('health_score')}")

    client.close()

if __name__ == "__main__":
    asyncio.run(check())
