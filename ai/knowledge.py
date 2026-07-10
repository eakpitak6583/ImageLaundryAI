from database.db import connect


def load_machine(model):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        brand,
        model,
        machine_type
    FROM machines
    WHERE model=?
    """, (model,))

    row = cursor.fetchone()

    conn.close()

    return row


def load_parts(model):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        part_no,
        description,
        page
    FROM parts
    WHERE model=?
    """, (model,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def load_repairs(model):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        complaint,
        detail,
        repair_action,
        result
    FROM repair_history
    WHERE machine_model=?
    """, (model,))

    rows = cursor.fetchall()

    conn.close()

    return rows