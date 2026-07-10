from db import connect


def update():

    conn = connect()
    cursor = conn.cursor()

    try:

        cursor.execute("""

        ALTER TABLE repair_history

        ADD COLUMN technician_id INTEGER

        """)

        conn.commit()

        print("technician_id added.")

    except Exception as e:

        print(e)

    conn.close()


if __name__ == "__main__":

    update()