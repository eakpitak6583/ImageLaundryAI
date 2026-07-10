import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from database.db import connect

conn = connect()
cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS machine_instances(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_id INTEGER,

    machine_id INTEGER,

    serial_no TEXT,

    sap_no TEXT,

    location TEXT,

    install_date TEXT,

    status TEXT DEFAULT 'ACTIVE',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")

conn.commit()

conn.close()

print("Machine Instance table created.")