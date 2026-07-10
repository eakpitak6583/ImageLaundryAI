from pathlib import Path
import sqlite3

DB = Path(__file__).resolve().parent / "laundry.db"

conn = sqlite3.connect(DB)

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS machine_master(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    machine_model TEXT,

    sap_no TEXT UNIQUE,

    serial_no TEXT,

    customer TEXT,

    location TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")

conn.commit()

conn.close()

print("machine_master created.")