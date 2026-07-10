from database.db import connect

conn = connect()
cursor = conn.cursor()

print("=== MACHINE MODEL ===")

cursor.execute("""
SELECT DISTINCT machine_model
FROM repair_history
ORDER BY machine_model
""")

for row in cursor.fetchall():
    print(row)

conn.close()