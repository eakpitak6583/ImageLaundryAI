"""
LaundryBot V7 Enterprise
Part Repository
"""

from repositories.base_repository import BaseRepository


class PartRepository(BaseRepository):

    # ==========================================================
    # Read
    # ==========================================================

    def get_all(self):

        return self.fetch_all("""
            SELECT *
            FROM parts
            ORDER BY model, part_no
        """)

    def get(self, part_id):

        return self.fetch_one("""
            SELECT *
            FROM parts
            WHERE id=?
        """, (part_id,))

    def get_by_model(self, model):

        return self.fetch_all("""
            SELECT *
            FROM parts
            WHERE model=?
            ORDER BY part_no
        """, (model,))

    def search(self, keyword):

        keyword = f"%{keyword}%"

        return self.fetch_all("""
            SELECT *
            FROM parts
            WHERE

                model LIKE ?

                OR part_no LIKE ?

                OR part_name LIKE ?

                OR location LIKE ?

            ORDER BY model, part_no
        """, (

            keyword,

            keyword,

            keyword,

            keyword,

        ))

    # ==========================================================
    # Create
    # ==========================================================

    def create(self, data):

        return self.execute("""

            INSERT INTO parts(

                part_no,

                part_name,

                model,

                stock,

                location

            )

            VALUES(?,?,?,?,?)

        """, (

            data.get("part_no"),

            data.get("part_name"),

            data.get("model"),

            data.get("stock"),

            data.get("location"),

        ))

    # ==========================================================
    # Update
    # ==========================================================

    def update(self, part_id, data):

        self.execute("""

            UPDATE parts

            SET

                part_no=?,

                part_name=?,

                model=?,

                stock=?,

                location=?

            WHERE id=?

        """, (

            data.get("part_no"),

            data.get("part_name"),

            data.get("model"),

            data.get("stock"),

            data.get("location"),

            part_id,

        ))

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(self, part_id):

        self.execute("""

            DELETE FROM parts

            WHERE id=?

        """, (

            part_id,

        ))


part_repository = PartRepository()