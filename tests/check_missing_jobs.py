from database.db import connect

conn = connect()
cursor = conn.cursor()

cursor.execute("""
SELECT job_no
FROM repair_history
ORDER BY job_no
""")

rows = cursor.fetchall()

print("จำนวน =", len(rows))

for r in rows:
    print(r[0])

conn.close()