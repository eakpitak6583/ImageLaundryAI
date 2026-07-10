"""
LaundryBot V5

Add customer_id to repair_history
"""

from db import connect


def add_customer_column():

    conn = connect()
    cursor = conn.cursor()

    try:

        cursor.execute("""

        ALTER TABLE repair_history

        ADD COLUMN customer_id INTEGER

        """)

        conn.commit()

        print("customer_id added successfully.")

    except Exception as e:

        print(e)

    conn.close()


if __name__ == "__main__":

    add_customer_column()