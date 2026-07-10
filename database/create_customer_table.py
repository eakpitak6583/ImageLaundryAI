from db import connect

conn = connect()
cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS customers (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_name TEXT UNIQUE,

    address TEXT,

    contact TEXT,

    phone TEXT,

    email TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")

conn.commit()

print("Customer table created successfully.")

conn.close()