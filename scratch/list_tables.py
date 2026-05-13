import sqlite3

db_path = r'C:\\Users\\USER\.gemini\antigravity\scratch\paisa\server\paisa.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables:", [t[0] for t in tables])
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()

