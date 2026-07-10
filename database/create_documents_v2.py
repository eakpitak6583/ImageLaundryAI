from database.db import connect

conn = connect()
cursor = conn.cursor()

cursor.execute("""
DROP TABLE IF EXISTS documents
""")

cursor.execute("""
CREATE TABLE documents (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    filename TEXT NOT NULL,

    document_type TEXT NOT NULL,

    model TEXT,

    category TEXT,

    page INTEGER,

    content TEXT,

    file_hash TEXT,

    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_documents_model
ON documents(model)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_documents_type
ON documents(document_type)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_documents_filename
ON documents(filename)
""")

conn.commit()
conn.close()

print("documents v2 created.")