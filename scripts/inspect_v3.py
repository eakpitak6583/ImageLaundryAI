import sqlite3

db = r"C:\Users\ACT-2021\Desktop\LaundryBotV3\database\laundry.db"

conn = sqlite3.connect(db)

tables = [
    "documents",
    "machines",
    "parts",
    "repair_history"
]

for table in tables:

    print("=" * 60)
    print(table)

    try:

        cols = conn.execute(
            f"PRAGMA table_info({table})"
        ).fetchall()

        for c in cols:
            print(c)

        count = conn.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]

        print("ROWS =", count)

    except Exception as e:
        print(e)

conn.close()