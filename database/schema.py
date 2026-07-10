import sqlite3
from pathlib import Path

# ==========================================
# Database Path
# ==========================================
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "laundry.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ==========================================
# Machines
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS machines (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    brand TEXT,

    model TEXT UNIQUE,

    machine_type TEXT,

    manual_file TEXT

)
""")

# ==========================================
# Manual Pages
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS manual_pages (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    model TEXT,

    page INTEGER,

    content TEXT

)
""")

# ==========================================
# Parts
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS parts (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    model TEXT,

    section TEXT,

    page INTEGER,

    item TEXT,

    part_no TEXT,

    qty TEXT,

    description TEXT

)
""")

# ==========================================
# Repair History
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS repair_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    job_no TEXT UNIQUE,

    machine_model TEXT,

    complaint TEXT,

    detail TEXT,

    repair_action TEXT,

    result TEXT,

    sap_no TEXT,

    serial_no TEXT,

    report_file TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

# ==========================================
# Repair Parts
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS repair_parts (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    job_no TEXT,

    part_no TEXT,

    description TEXT,

    qty TEXT

)
""")

# ==========================================
# Index
# ==========================================
cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_parts_model
ON parts(model)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_parts_partno
ON parts(part_no)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_repair_model
ON repair_history(machine_model)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_repair_job
ON repair_history(job_no)
""")
# ------------------------
# Users
# ------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE NOT NULL,

    password TEXT NOT NULL,

    fullname TEXT,

    email TEXT,

    role TEXT NOT NULL DEFAULT 'technician',

    active INTEGER NOT NULL DEFAULT 1,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()
conn.close()

print("=" * 60)
print("LaundryBot Database Created Successfully")
print(DB_PATH)
print("=" * 60)