from db import connect


def create_technician_table():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS technicians(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        fullname TEXT UNIQUE,

        phone TEXT,

        email TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    conn.commit()
    conn.close()

    print("Technician table created.")


if __name__ == "__main__":

    create_technician_table()