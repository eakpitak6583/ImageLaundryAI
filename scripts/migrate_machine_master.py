"""
LaundryBot V7 Enterprise
Machine Master Migration
"""

import sqlite3
import sys
from pathlib import Path

# ==========================================================
# Add Project Root
# ==========================================================

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import Config

# ==========================================================
# Connect Database
# ==========================================================

conn = sqlite3.connect(Config.DATABASE_PATH)

cur = conn.cursor()

# ==========================================================
# Create Machine Master Table
# ==========================================================

cur.execute("""
CREATE TABLE IF NOT EXISTS machine_master(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    brand TEXT NOT NULL,

    model TEXT NOT NULL UNIQUE,

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

    parts_file TEXT,

    image_file TEXT,

    description TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

# ==========================================================
# Create Index
# ==========================================================

cur.execute("""
CREATE INDEX IF NOT EXISTS idx_machine_master_model
ON machine_master(model)
""")

cur.execute("""
CREATE INDEX IF NOT EXISTS idx_machine_master_brand
ON machine_master(brand)
""")

# ==========================================================
# Commit
# ==========================================================

conn.commit()

conn.close()

# ==========================================================
# Result
# ==========================================================

print("=" * 60)
print("LaundryBot V7 Enterprise")
print("Machine Master Migration Completed")
print(f"Database : {Config.DATABASE_PATH}")
print("=" * 60)