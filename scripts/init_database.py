"""
LaundryBot V7 Enterprise
Initialize Database
"""

import sqlite3
import sys
from pathlib import Path

# ==========================================================
# Project Path
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(BASE_DIR))

from config import Config


# ==========================================================
# Create Folder
# ==========================================================

Config.DATABASE_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)


# ==========================================================
# Connect Database
# ==========================================================

conn = sqlite3.connect(Config.DATABASE_PATH)

conn.execute("PRAGMA foreign_keys = ON")

cur = conn.cursor()


# ==========================================================
# USERS
# ==========================================================

cur.execute("""

CREATE TABLE IF NOT EXISTS users(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE NOT NULL,

    password TEXT NOT NULL,

    fullname TEXT,

    email TEXT,

    role TEXT DEFAULT 'user',

    active INTEGER DEFAULT 1,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")


# ==========================================================
# CUSTOMERS
# ==========================================================

cur.execute("""

CREATE TABLE IF NOT EXISTS customers(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_name TEXT NOT NULL,

    address TEXT,

    contact TEXT,

    phone TEXT,

    email TEXT,

    note TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")
# ==========================================================
# MACHINE MASTER
# ==========================================================

cur.execute("""

CREATE TABLE IF NOT EXISTS machine_master(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    brand TEXT NOT NULL,

    model TEXT NOT NULL,

    machine_type TEXT,

    category TEXT,

    capacity TEXT,

    fuel_type TEXT,

    voltage TEXT,

    phase TEXT,

    frequency TEXT,

    manufacturer TEXT,

    country TEXT,

    manual_file TEXT,

    image_file TEXT,

    description TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")


# ==========================================================
# MACHINE INSTANCES
# ==========================================================

cur.execute("""

CREATE TABLE IF NOT EXISTS machine_instances(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    machine_master_id INTEGER NOT NULL,

    serial_number TEXT UNIQUE,

    asset_code TEXT,

    customer_id INTEGER,

    location TEXT,

    install_date TEXT,

    warranty_expire TEXT,

    status TEXT DEFAULT 'Running',

    running_hour REAL DEFAULT 0,

    note TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(machine_master_id)

        REFERENCES machine_master(id),

    FOREIGN KEY(customer_id)

        REFERENCES customers(id)

)

""")


# ==========================================================
# MACHINES (Legacy Compatibility)
# ==========================================================

cur.execute("""

CREATE TABLE IF NOT EXISTS machines(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    brand TEXT,

    model TEXT,

    machine_type TEXT,

    manual_file TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")
# ==========================================================
# PARTS
# ==========================================================

cur.execute("""

CREATE TABLE IF NOT EXISTS parts(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    model TEXT,

    section TEXT,

    item TEXT,

    part_no TEXT,

    description TEXT,

    qty INTEGER DEFAULT 0,

    remark TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")


# ==========================================================
# REPAIR HISTORY
# ==========================================================

cur.execute("""

CREATE TABLE IF NOT EXISTS repair_history(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    job_no TEXT,

    machine_model TEXT,

    complaint TEXT,

    detail TEXT,

    repair_action TEXT,

    result TEXT,

    sap_no TEXT,

    serial_no TEXT,

    report_file TEXT,

    customer_id INTEGER,

    technician_id INTEGER,

    machine_id INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(customer_id)
        REFERENCES customers(id),

    FOREIGN KEY(technician_id)
        REFERENCES technicians(id),

    FOREIGN KEY(machine_id)
        REFERENCES machine_instances(id)

)

""")


# ==========================================================
# REPAIR PARTS
# ==========================================================

cur.execute("""

CREATE TABLE IF NOT EXISTS repair_parts(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    repair_id INTEGER NOT NULL,

    part_id INTEGER NOT NULL,

    qty INTEGER DEFAULT 1,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(repair_id)
        REFERENCES repair_history(id)
        ON DELETE CASCADE,

    FOREIGN KEY(part_id)
        REFERENCES parts(id)

)

""")
# ==========================================================
# DOCUMENTS
# ==========================================================

cur.execute("""

CREATE TABLE IF NOT EXISTS documents(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    filename TEXT NOT NULL,

    document_type TEXT,

    model TEXT,

    category TEXT,

    page INTEGER,

    content TEXT,

    file_hash TEXT,

    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")


# ==========================================================
# IMPORT LOGS
# ==========================================================

cur.execute("""

CREATE TABLE IF NOT EXISTS import_logs(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    filename TEXT,

    document_type TEXT,

    status TEXT,

    records INTEGER DEFAULT 0,

    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")


# ==========================================================
# TECHNICIANS
# ==========================================================

cur.execute("""

CREATE TABLE IF NOT EXISTS technicians(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    phone TEXT,

    email TEXT,

    position TEXT,

    note TEXT,

    active INTEGER DEFAULT 1,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")


# ==========================================================
# SETTINGS
# ==========================================================

cur.execute("""

CREATE TABLE IF NOT EXISTS settings(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    config_key TEXT UNIQUE,

    config_value TEXT,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")


# ==========================================================
# AI CHAT HISTORY
# ==========================================================

cur.execute("""

CREATE TABLE IF NOT EXISTS ai_chat_history(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    question TEXT,

    answer TEXT,

    username TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")
# ==========================================================
# INDEX
# ==========================================================

indexes = [

    "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)",

    "CREATE INDEX IF NOT EXISTS idx_customer_name ON customers(customer_name)",

    "CREATE INDEX IF NOT EXISTS idx_machine_master_brand ON machine_master(brand)",

    "CREATE INDEX IF NOT EXISTS idx_machine_master_model ON machine_master(model)",

    "CREATE INDEX IF NOT EXISTS idx_machine_instance_serial ON machine_instances(serial_number)",

    "CREATE INDEX IF NOT EXISTS idx_machine_instance_customer ON machine_instances(customer_id)",

    "CREATE INDEX IF NOT EXISTS idx_parts_model ON parts(model)",

    "CREATE INDEX IF NOT EXISTS idx_parts_partno ON parts(part_no)",

    "CREATE INDEX IF NOT EXISTS idx_repair_job ON repair_history(job_no)",

    "CREATE INDEX IF NOT EXISTS idx_repair_machine ON repair_history(machine_id)",

    "CREATE INDEX IF NOT EXISTS idx_documents_model ON documents(model)",

    "CREATE INDEX IF NOT EXISTS idx_documents_filename ON documents(filename)",

]

for sql in indexes:

    cur.execute(sql)


# ==========================================================
# DEFAULT SETTINGS
# ==========================================================

defaults = [

    ("system_name", "LaundryBot V7 Enterprise"),

    ("version", "7.0"),

    ("ai_model", Config.MODEL_NAME),

]

for key, value in defaults:

    cur.execute("""

        INSERT OR IGNORE INTO settings(

            config_key,

            config_value

        )

        VALUES(?,?)

    """, (key, value))


# ==========================================================
# Commit
# ==========================================================

conn.commit()

conn.close()


# ==========================================================
# Done
# ==========================================================

print("=" * 60)
print("LaundryBot V7 Enterprise")
print("Database Initialized Successfully")
print("Database :", Config.DATABASE_PATH)
print("=" * 60)