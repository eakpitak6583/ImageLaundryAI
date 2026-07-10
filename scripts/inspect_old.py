import sqlite3

db = r"C:\Users\ACT-2021\Desktop\LaundryBot\database\laundry.db"

conn = sqlite3.connect(db)

tables = conn.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name
""").fetchall()

print("=" * 60)
print("DATABASE :", db)
print("=" * 60)

for t in tables:

    table = t[0]

    print("\n" + "=" * 60)
    print(table)

    cols = conn.execute(
        f"PRAGMA table_info({table})"
    ).fetchall()

    for c in cols:
        print(c)

    count = conn.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print("ROWS =", count)

conn.close()