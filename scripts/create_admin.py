"""
LaundryBot V7 Enterprise
Create Admin User
"""

import sys
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from werkzeug.security import generate_password_hash
from config import Config

conn = sqlite3.connect(Config.DATABASE_PATH)

cur = conn.cursor()

# ตรวจสอบว่ามี admin แล้วหรือยัง
row = cur.execute(
    """
    SELECT id
    FROM users
    WHERE username=?
    """,
    ("admin",)
).fetchone()

if row:

    print("Admin already exists.")

else:

    cur.execute(
        """
        INSERT INTO users
        (
            username,
            password,
            fullname,
            role
        )
        VALUES
        (
            ?, ?, ?, ?
        )
        """,
        (
            "admin",
            generate_password_hash("admin123"),
            "System Administrator",
            "admin",
        ),
    )

    conn.commit()

    print("=" * 60)
    print("Admin Created")
    print("Username : admin")
    print("Password : admin123")
    print("=" * 60)

conn.close()