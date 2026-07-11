"""
LaundryBot V7 Enterprise
Database Index Migration
"""

from pathlib import Path
import sqlite3
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from config import Config


def create_index(conn, name, sql):

    rows = conn.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='index'
    """).fetchall()

    exists = any(r[0] == name for r in rows)

    if exists:

        print(f"[SKIP] {name}")
        return

    print(f"[ADD ] {name}")

    conn.execute(sql)


def migrate():

    conn = sqlite3.connect(Config.DATABASE_PATH)

    print("=" * 60)
    print("LaundryBot V8 Index Migration")
    print("=" * 60)

    create_index(

        conn,

        "idx_customer_name",

        """
        CREATE INDEX idx_customer_name
        ON customers(customer_name)
        """

    )

    create_index(

        conn,

        "idx_machine_model",

        """
        CREATE INDEX idx_machine_model
        ON machines(model)
        """

    )

    create_index(

        conn,

        "idx_machine_sap",

        """
        CREATE INDEX idx_machine_sap
        ON machines(sap_no)
        """

    )

    create_index(

        conn,

        "idx_machine_serial",

        """
        CREATE INDEX idx_machine_serial
        ON machines(serial_no)
        """

    )

    create_index(

        conn,

        "idx_repair_job",

        """
        CREATE INDEX idx_repair_job
        ON repair_history(job_no)
        """

    )

    create_index(

        conn,

        "idx_repair_machine",

        """
        CREATE INDEX idx_repair_machine
        ON repair_history(machine_id)
        """

    )

    create_index(

        conn,

        "idx_repair_customer",

        """
        CREATE INDEX idx_repair_customer
        ON repair_history(customer_id)
        """

    )

    create_index(

        conn,

        "idx_repair_technician",

        """
        CREATE INDEX idx_repair_technician
        ON repair_history(technician_id)
        """

    )

    conn.commit()

    conn.close()

    print("=" * 60)
    print("Index Migration Completed")
    print("=" * 60)


if __name__ == "__main__":

    migrate()