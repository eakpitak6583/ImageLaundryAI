from database.db import connect

conn = connect()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS import_logs (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    filename TEXT,

    document_type TEXT,

    status TEXT,

    records INTEGER,

    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()
conn.close()

print("import_logs table created.")