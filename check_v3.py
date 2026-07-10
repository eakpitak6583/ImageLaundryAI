import sqlite3

db = r"C:\Users\ACT-2021\Desktop\LaundryBotV3\database\laundry.db"

conn = sqlite3.connect(db)

rows = conn.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name
""").fetchall()

print("TABLES")

for r in rows:
    print("-", r[0])

conn.close()