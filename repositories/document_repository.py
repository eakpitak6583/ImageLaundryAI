"""
Image Laundry AI
Document Repository
"""

from repositories.base_repository import BaseRepository


class DocumentRepository(BaseRepository):

    # ==========================================================
    # Read
    # ==========================================================

    def get_all(self):

        return self.fetch_all("""

            SELECT *

            FROM documents

            ORDER BY imported_at DESC,
                     filename,
                     page

        """)

    def get(self, document_id):

        return self.fetch_one("""

            SELECT *

            FROM documents

            WHERE id = ?

        """, (

            document_id,

        ))

    def search(self, keyword):

        keyword = f"%{keyword}%"

        return self.fetch_all("""

            SELECT *

            FROM documents

            WHERE

                filename LIKE ?

                OR model LIKE ?

                OR category LIKE ?

                OR document_type LIKE ?

                OR content LIKE ?

            ORDER BY imported_at DESC,
                     filename,
                     page

        """, (

            keyword,

            keyword,

            keyword,

            keyword,

            keyword,

        ))
    # ==========================================================
    # Import Logs
    # ==========================================================

    def import_logs(

        self,

    ):

        return self.fetch_all(

            """

            SELECT *

            FROM import_logs

            ORDER BY

                imported_at DESC,

                id DESC

            """

        )
    # ==========================================================
    # Find By Hash
    # ==========================================================

    def find_by_hash(

        self,

        file_hash,

    ):

        if not file_hash:

            return None

        return self.fetch_one(

            """

            SELECT *

            FROM documents

            WHERE file_hash = ?

            LIMIT 1

            """,

            (

                file_hash,

            ),

        )
    # ==========================================================
    # Latest
    # ==========================================================

    def latest(

        self,

        limit=20,

    ):

        return self.fetch_all(

            """

            SELECT *

            FROM documents

            ORDER BY

                imported_at DESC,

                id DESC

            LIMIT ?

            """,

            (

                limit,

            ),

        )
    # ==========================================================
    # Statistics
    # ==========================================================

    def total(

        self,

    ):

        row = self.fetch_one(

            """

            SELECT

                COUNT(*) AS total

            FROM documents

            """

        )

        if row is None:

            return 0

        return row["total"]

    # ==========================================================
    # Create
    # ==========================================================

    def create(self, data):

        return self.execute("""

            INSERT INTO documents
            (

                filename,

                document_type,

                model,

                category,

                page,

                content,

                file_hash

            )

            VALUES
            (
                ?, ?, ?, ?, ?, ?, ?
            )

        """, (

            data.get("filename"),

            data.get("document_type"),

            data.get("model"),

            data.get("category"),

            data.get("page"),

            data.get("content"),

            data.get("file_hash"),

        ))

    # ==========================================================
    # Update
    # ==========================================================

    def update(self, document_id, data):

        self.execute("""

            UPDATE documents

            SET

                filename = ?,

                document_type = ?,

                model = ?,

                category = ?,

                page = ?,

                content = ?,

                file_hash = ?

            WHERE id = ?

        """, (

            data.get("filename"),

            data.get("document_type"),

            data.get("model"),

            data.get("category"),

            data.get("page"),

            data.get("content"),

            data.get("file_hash"),

            document_id,

        ))

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(self, document_id):

        self.execute("""

            DELETE FROM documents

            WHERE id = ?

        """, (

            document_id,

        ))

    # ==========================================================
    # Exists
    # ==========================================================

    def exists(

        self,

        file_hash,

    ):

        return self.find_by_hash(

            file_hash,

        ) is not None
        


document_repository = DocumentRepository()