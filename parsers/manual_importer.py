from database.db import connect
from parsers.pdf_reader import read_pdf


def import_manual_pdf(file_path):

    pages = read_pdf(file_path)

    conn = connect()
    cursor = conn.cursor()

    total = 0

    for p in pages:

        # -----------------------------
        # documents
        # -----------------------------
        cursor.execute(
            """
            INSERT INTO documents
            (
                filename,
                document_type,
                page,
                content
            )
            VALUES
            (
                ?, ?, ?, ?
            )
            """,
            (
                file_path.name,
                "manual",
                p["page"],
                p["text"],
            ),
        )

        # -----------------------------
        # manual_pages
        # -----------------------------
        cursor.execute(
            """
            INSERT INTO manual_pages
            (
                model,
                page,
                content
            )
            VALUES
            (
                ?, ?, ?
            )
            """,
            (
                "",
                p["page"],
                p["text"],
            ),
        )

        total += 1

    conn.commit()
    conn.close()

    return total