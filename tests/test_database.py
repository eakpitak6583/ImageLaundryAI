from database.db import connect

conn = connect()
cursor = conn.cursor()

tables = [
    "machines",
    "parts",
    "manual_pages",
    "repair_history"
]

for table in tables:

    cursor.execute(f"SELECT COUNT(*) FROM {table}")

    count = cursor.fetchone()[0]

    print(f"{table:20} : {count}")

conn.close()