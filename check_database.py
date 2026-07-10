from config import Config
import sqlite3
import os

print("=" * 60)
print("DATABASE PATH")
print(Config.DATABASE_PATH)
print("=" * 60)

print("EXISTS :", os.path.exists(Config.DATABASE_PATH))
print("SIZE   :", os.path.getsize(Config.DATABASE_PATH), "bytes")

conn = sqlite3.connect(Config.DATABASE_PATH)

tables = conn.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name
""").fetchall()

print("\nTABLES")

for t in tables:
    print("-", t[0])

conn.close()