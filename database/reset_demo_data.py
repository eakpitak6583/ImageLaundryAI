from db import connect
conn = connect()
cursor = conn.cursor()

tables = [
    "repair_history",
    "machine_master",
    "customers",
    "technicians",
]

for table in tables:
    cursor.execute(f"DELETE FROM {table}")
    print(f"Cleared {table}")

conn.commit()
conn.close()

print("Database reset completed.")