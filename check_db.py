from config import Config
from database.db import connect

print("DATABASE =", Config.DATABASE_PATH)

conn = connect()

tables = conn.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name
""").fetchall()

print("\nTABLES")

for t in tables:
    print("-", t["name"])