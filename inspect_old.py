import sqlite3

db = r"C:\Users\ACT-2021\Desktop\LaundryBot\database\laundry.db"

conn = sqlite3.connect(db)

tables = conn.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name
""").fetchall()

print("TABLES")

for t in tables:

    print("\n========================")
    print(t[0])

    cols = conn.execute(
        f"PRAGMA table_info({t[0]})"
    ).fetchall()

    for c in cols:
        print(c)

    count = conn.execute(
        f"SELECT COUNT(*) FROM {t[0]}"
    ).fetchone()[0]

    print("ROWS =", count)

conn.close()