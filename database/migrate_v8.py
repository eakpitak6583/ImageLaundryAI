"""
LaundryBot V7 Enterprise
Database Migration V8
"""

from pathlib import Path
import sqlite3
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from config import Config


# ==========================================================
# Helper
# ==========================================================

def column_exists(conn, table, column):

    rows = conn.execute(
        f"PRAGMA table_info({table})"
    ).fetchall()

    return any(r[1] == column for r in rows)


def add_column(conn, table, column, sql_type):

    if column_exists(conn, table, column):

        print(f"[SKIP] {table}.{column}")

        return

    print(f"[ADD ] {table}.{column}")

    conn.execute(
        f"""
        ALTER TABLE {table}
        ADD COLUMN {column} {sql_type}
        """
    )


# ==========================================================
# Migration
# ==========================================================

def migrate():

    conn = sqlite3.connect(Config.DATABASE_PATH)

    print("=" * 60)
    print("LaundryBot V8 Database Migration")
    print("=" * 60)

    # ------------------------------------------------------
    # machines
    # ------------------------------------------------------

    add_column(
        conn,
        "machines",
        "sap_no",
        "TEXT",
    )

    add_column(
        conn,
        "machines",
        "serial_no",
        "TEXT",
    )

    add_column(
        conn,
        "machines",
        "customer_id",
        "INTEGER",
    )

    add_column(
        conn,
        "machines",
        "machine_master_id",
        "INTEGER",
    )

    add_column(
        conn,
        "machines",
        "location",
        "TEXT",
    )

    add_column(
        conn,
        "machines",
        "status",
        "TEXT DEFAULT 'ACTIVE'",
    )

    add_column(
        conn,
        "machines",
        "install_date",
        "TEXT",
    )

    add_column(
        conn,
        "machines",
        "note",
        "TEXT",
    )

    # ------------------------------------------------------
    # repair_history
    # ------------------------------------------------------

    add_column(
        conn,
        "repair_history",
        "repair_date",
        "TEXT",
    )

    add_column(
        conn,
        "repair_history",
        "downtime",
        "REAL",
    )

    add_column(
        conn,
        "repair_history",
        "cost",
        "REAL",
    )

    add_column(
        conn,
        "repair_history",
        "parts_used",
        "TEXT",
    )

    add_column(
        conn,
        "repair_history",
        "failure_code",
        "TEXT",
    )

    add_column(
        conn,
        "repair_history",
        "priority",
        "TEXT",
    )

    add_column(
        conn,
        "repair_history",
        "status",
        "TEXT DEFAULT 'COMPLETED'",
    )

    add_column(
        conn,
        "repair_history",
        "document_type",
        "TEXT",
    )

    # ------------------------------------------------------
    # technicians
    # ------------------------------------------------------

    add_column(
        conn,
        "technicians",
        "employee_code",
        "TEXT",
    )

    add_column(
        conn,
        "technicians",
        "department",
        "TEXT",
    )

    # ------------------------------------------------------
    # customers
    # ------------------------------------------------------

    add_column(
        conn,
        "customers",
        "customer_code",
        "TEXT",
    )

    # ------------------------------------------------------

    conn.commit()

    conn.close()

    print("=" * 60)
    print("Migration Completed")
    print("=" * 60)


if __name__ == "__main__":

    migrate()