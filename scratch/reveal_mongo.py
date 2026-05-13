import sys
import os

# Ensure we can import core.database
sys.path.append("C:\Users\USER/.gemini/antigravity/scratch/paisa/server")

from core.database import MONGO_URI, DB_NAME

print(f"MONGO_URI: {MONGO_URI}")
print(f"DB_NAME: {DB_NAME}")

