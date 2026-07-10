"""
LaundryBot V7 Enterprise
Technician Repository
"""

from repositories.base_repository import BaseRepository


class TechnicianRepository(BaseRepository):

    # ==========================================================
    # Read
    # ==========================================================

    def get_all(self):

        return self.fetch_all("""
            SELECT *
            FROM technicians
            ORDER BY fullname
        """)

    def get(self, technician_id):

        return self.fetch_one("""
            SELECT *
            FROM technicians
            WHERE id = ?
        """, (technician_id,))

    def search(self, keyword):

        keyword = f"%{keyword}%"

        return self.fetch_all("""
            SELECT *
            FROM technicians
            WHERE
                fullname LIKE ?
                OR phone LIKE ?
                OR email LIKE ?
            ORDER BY fullname
        """, (
            keyword,
            keyword,
            keyword
        ))

    # ==========================================================
    # Create
    # ==========================================================

    def create(self, data):

        sql = """
        INSERT INTO technicians
        (
            fullname,
            phone,
            email
        )
        VALUES
        (
            ?, ?, ?
        )
        """

        return self.execute(sql, (

            data.get("fullname"),
            data.get("phone"),
            data.get("email")

        ))

    # ==========================================================
    # Update
    # ==========================================================

    def update(self, technician_id, data):

        sql = """
        UPDATE technicians
        SET

            fullname=?,
            phone=?,
            email=?

        WHERE id=?
        """

        self.execute(sql, (

            data.get("fullname"),
            data.get("phone"),
            data.get("email"),
            technician_id

        ))

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(self, technician_id):

        self.execute("""
            DELETE FROM technicians
            WHERE id=?
        """, (technician_id,))


technician_repository = TechnicianRepository()