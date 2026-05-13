from pymongo import MongoClient
import sys

def test_mongo():
    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        print("MongoDB is UP")
    except Exception as e:
        print(f"MongoDB is DOWN: {e}")

if __name__ == "__main__":
    test_mongo()
