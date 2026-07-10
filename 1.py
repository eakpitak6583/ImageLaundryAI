from database.db import connect

conn = connect()

print("documents")

rows = conn.execute("""
SELECT COUNT(*)
FROM documents
""").fetchone()

print(rows[0])

print()

print("document_files")

rows = conn.execute("""
SELECT id,name
FROM document_files
""").fetchall()

for r in rows:
    print(r)