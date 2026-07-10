"""
LaundryBot V7 Enterprise
Migrate Database V3 -> V7
"""

import sqlite3
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from config import Config

# -----------------------------
# Source (V3)
# -----------------------------
SOURCE_DB = r"C:\Users\ACT-2021\Desktop\LaundryBotV3\database\laundry.db"

# -----------------------------
# Destination (V7)
# -----------------------------
DEST_DB = str(Config.DATABASE_PATH)

src = sqlite3.connect(SOURCE_DB)
src.row_factory = sqlite3.Row

dst = sqlite3.connect(DEST_DB)

print("=" * 60)
print("SOURCE :", SOURCE_DB)
print("DEST   :", DEST_DB)
print("=" * 60)


def copy_table(source_table, dest_table, columns):

    try:

        rows = src.execute(
            f"SELECT {','.join(columns)} FROM {source_table}"
        ).fetchall()

        if not rows:
            print(f"{source_table} : 0 rows")
            return

        placeholders = ",".join(["?"] * len(columns))

        dst.executemany(

            f"""
            INSERT INTO {dest_table}
            ({','.join(columns)})
            VALUES ({placeholders})
            """,

            [tuple(r[c] for c in columns) for r in rows]

        )

        print(f"{source_table} : {len(rows)} rows")

    except Exception as e:

        print(f"{source_table} : ERROR")

        print(e)


# ==========================================================
# DOCUMENTS
# ==========================================================

copy_table(

    "documents",

    "documents",

    [

        "filename",

        "document_type",

        "model",

        "category",

        "page",

        "content",

        "file_hash",

        "imported_at",

    ],

)

# ==========================================================
# MACHINES
# ==========================================================

try:

    rows = src.execute(

        "SELECT * FROM machines"

    ).fetchall()

    for r in rows:

        dst.execute(

            """
            INSERT INTO machines(

                machine_name,

                model

            )

            VALUES(?,?)

            """,

            (

                r["machine_name"],

                r["model"],

            ),

        )

    print(f"machines : {len(rows)} rows")

except Exception as e:

    print(e)

# ==========================================================
# PARTS
# ==========================================================

try:

    rows = src.execute(

        "SELECT * FROM parts"

    ).fetchall()

    for r in rows:

        dst.execute(

            """
            INSERT INTO parts(

                part_no,

                part_name,

                model

            )

            VALUES(?,?,?)

            """,

            (

                r["part_no"],

                r["part_name"],

                r["model"],

            ),

        )

    print(f"parts : {len(rows)} rows")

except Exception as e:

    print(e)

# ==========================================================
# REPAIR HISTORY
# ==========================================================

try:

    rows = src.execute(

        "SELECT * FROM repair_history"

    ).fetchall()

    for r in rows:

        dst.execute(

            """
            INSERT INTO repair_history(

                machine_id,

                repair_date,

                symptom,

                cause,

                solution,

                technician,

                downtime

            )

            VALUES(?,?,?,?,?,?,?)

            """,

            (

                r["machine_id"],

                r["repair_date"],

                r["symptom"],

                r["cause"],

                r["solution"],

                r["technician"],

                r["downtime"],

            ),

        )

    print(f"repair_history : {len(rows)} rows")

except Exception as e:

    print(e)

dst.commit()

src.close()
dst.close()

print("=" * 60)
print("Migration Completed")
print("=" * 60)