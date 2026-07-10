from database.db import connect
from parsers.pdf_reader import read_pdf


def import_summary_pdf(file_path):

    pages = read_pdf(file_path)

    conn = connect()
    cursor = conn.cursor()

    for page in pages:

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
            (?, ?, ?, ?)
            """,
            (
                file_path.name,
                "summary_report",
                page["page"],
                page["text"],
            ),
        )

    conn.commit()
    conn.close()

    return len(pages)