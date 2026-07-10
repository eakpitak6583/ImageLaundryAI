from db import connect

conn = connect()

cursor = conn.cursor()

try:

    cursor.execute("""

        ALTER TABLE repair_history

        ADD COLUMN technician_id INTEGER

    """)

except:

    pass

try:

    cursor.execute("""

        ALTER TABLE repair_history

        ADD COLUMN customer_id INTEGER

    """)

except:

    pass

conn.commit()

conn.close()

print("Repair table updated.")