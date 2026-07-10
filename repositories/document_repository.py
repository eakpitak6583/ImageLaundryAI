"""
LaundryBot V7 Enterprise
Document Repository
"""

from database.db import connect


class DocumentRepository:

    def create(
        self,
        filename,
        filepath,
        document_type,
        model,
        category,
        filesize,
        uploaded_by,
    ):

        conn = connect()

        conn.execute(
            """
            INSERT INTO document_files
            (
                filename,
                filepath,
                document_type,
                model,
                category,
                filesize,
                uploaded_by
            )
            VALUES
            (
                ?,?,?,?,?,?,?
            )
            """,
            (
                filename,
                filepath,
                document_type,
                model,
                category,
                filesize,
                uploaded_by,
            ),
        )

        conn.commit()

    def get_all(self):

        conn = connect()

        return conn.execute(
            """
            SELECT *
            FROM document_files
            ORDER BY uploaded_at DESC
            """
        ).fetchall()

    def get(self, document_id):

        conn = connect()

        return conn.execute(
            """
            SELECT *
            FROM document_files
            WHERE id=?
            """,
            (document_id,),
        ).fetchone()

    def delete(self, document_id):

        conn = connect()

        conn.execute(
            """
            DELETE
            FROM document_files
            WHERE id=?
            """,
            (document_id,),
        )

        conn.commit()


document_repository = DocumentRepository()