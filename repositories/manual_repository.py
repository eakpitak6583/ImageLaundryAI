"""
LaundryBot V7 Enterprise
Manual Repository
"""

from repositories.base_repository import BaseRepository


class ManualRepository(BaseRepository):

    # ==========================================================
    # Manual List
    # ==========================================================

    def get_all(self):

        return self.fetch_all(
            """
            SELECT

                filename,

                document_type,

                model,

                COUNT(*) AS total_pages,

                MIN(id) AS id

            FROM documents

            WHERE document_type='manual'

            GROUP BY

                filename,

                document_type,

                model

            ORDER BY filename
            """
        )


    # ==========================================================
    # Manual Detail
    # ==========================================================

    def get(self, manual_id):

        return self.fetch_all(
            """
            SELECT *

            FROM documents

            WHERE filename=(

                SELECT filename

                FROM documents

                WHERE id=?

            )

            ORDER BY page
            """,
            (
                manual_id,
            ),
        )


    # ==========================================================
    # Search
    # ==========================================================

    def search(self, keyword):

        keyword = f"%{keyword}%"

        return self.fetch_all(
            """
            SELECT

                filename,

                document_type,

                model,

                COUNT(*) AS total_pages,

                MIN(id) AS id

            FROM documents

            WHERE

                document_type='manual'

                AND

                (

                    filename LIKE ?

                    OR model LIKE ?

                    OR content LIKE ?

                )

            GROUP BY

                filename,

                document_type,

                model

            ORDER BY filename
            """,
            (
                keyword,
                keyword,
                keyword,
            ),
        )


    # ==========================================================
    # Model
    # ==========================================================

    def get_by_model(self, model):

        return self.fetch_all(
            """
            SELECT *

            FROM documents

            WHERE

                document_type='manual'

                AND model=?

            ORDER BY page
            """,
            (
                model,
            ),
        )


manual_repository = ManualRepository()