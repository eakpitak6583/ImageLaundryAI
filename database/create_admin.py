from flask_bcrypt import Bcrypt

from database.db import connect

bcrypt = Bcrypt()

conn = connect()
cursor = conn.cursor()

username = "admin"

password = bcrypt.generate_password_hash(
    "admin123"
).decode("utf-8")

cursor.execute("""
SELECT id
FROM users
WHERE username=?
""", (username,))

exists = cursor.fetchone()

if exists:

    print("Admin already exists")

else:

    cursor.execute("""
    INSERT INTO users(

        username,

        password,

        fullname,

        email,

        role

    )

    VALUES(

        ?,?,?,?,?

    )
    """,

    (

        "admin",

        password,

        "System Administrator",

        "admin@laundrybot.local",

        "admin",

    ))

    conn.commit()

    print("Admin Created")

conn.close()