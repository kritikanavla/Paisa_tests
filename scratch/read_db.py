import sqlite3
import json

db_path = r'C:\\Users\\USER\.gemini\antigravity\scratch\paisa\server\paisa.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

try:
    cursor.execute("SELECT * FROM trades")
    rows = cursor.fetchall()
    trades = [dict(row) for row in rows]
    print(json.dumps(trades, indent=2))
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()

