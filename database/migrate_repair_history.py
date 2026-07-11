"""
LaundryBot V7 Enterprise
Repair History Database Migration
"""

import sqlite3

from config import Config


def column_exists(conn, table, column):

    columns = conn.execute(
        f"PRAGMA table_info({table})"
    ).fetchall()

    return any(c[1] == column for c in columns)


def add_column(conn, table, column, sql_type):

    if not column_exists(conn, table, column):

        print(f"ADD COLUMN : {column}")

        conn.execute(
            f"""
            ALTER TABLE {table}
            ADD COLUMN {column} {sql_type}
            """
        )


def migrate():

    conn = sqlite3.connect(Config.DATABASE_PATH)

    print("=" * 60)
    print("Repair History Migration")
    print("=" * 60)

    add_column(
        conn,
        "repair_history",
        "customer",
        "TEXT",
    )

    add_column(
        conn,
        "repair_history",
        "department",
        "TEXT",
    )

    add_column(
        conn,
        "repair_history",
        "technician",
        "TEXT",
    )

    add_column(
        conn,
        "repair_history",
        "repair_date",
        "TEXT",
    )

    add_column(
        conn,
        "repair_history",
        "machine_name",
        "TEXT",
    )

    add_column(
        conn,
        "repair_history",
        "document_type",
        "TEXT",
    )

    conn.commit()

    conn.close()

    print("=" * 60)
    print("Migration Completed")
    print("=" * 60)


if __name__ == "__main__":

    migrate()