import sqlite3

conn = sqlite3.connect("database/laundry.db")

print("=" * 60)

for row in conn.execute("PRAGMA table_info(repair_history)"):
    print(row)

print("=" * 60)