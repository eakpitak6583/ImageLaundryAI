from database.db import connect

conn = connect()
cursor = conn.cursor()

print("=== MODEL ===")

cursor.execute("""
SELECT DISTINCT model
FROM parts
LIMIT 20
""")

for row in cursor.fetchall():
    print(row)

print()

print("=== STEAM ===")

cursor.execute("""
SELECT
    part_no,
    description
FROM parts
WHERE description LIKE '%steam%'
LIMIT 20
""")

for row in cursor.fetchall():
    print(row)

conn.close()