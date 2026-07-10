"""
Image Laundry AI
User Repository
"""

from repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):

    # ==========================================================
    # Read
    # ==========================================================

    def get_all(self):

        return self.fetch_all("""
            SELECT *
            FROM users
            ORDER BY fullname
        """)

    def get(self, user_id):

        return self.fetch_one("""
            SELECT *
            FROM users
            WHERE id = ?
        """, (user_id,))

    def find_by_username(self, username):

        return self.fetch_one("""
            SELECT *
            FROM users
            WHERE username = ?
        """, (username,))

    def login(self, username):
        """
        Authentication

        การตรวจสอบ Password
        ทำใน AuthService
        """

        return self.fetch_one("""
            SELECT *
            FROM users
            WHERE username = ?
        """, (username,))

    # ==========================================================
    # Create
    # ==========================================================

    def create(self, data):

        sql = """
        INSERT INTO users
        (
            username,
            password,
            fullname,
            role
        )
        VALUES
        (
            ?, ?, ?, ?
        )
        """

        return self.execute(sql, (

            data["username"],

            data["password"],

            data.get("fullname"),

            data.get("role", "technician"),

        ))

    # ==========================================================
    # Update
    # ==========================================================

    def update(self, user_id, data):

        sql = """
        UPDATE users
        SET
            fullname = ?,
            role = ?
        WHERE id = ?
        """

        self.execute(sql, (

            data.get("fullname"),

            data.get("role"),

            user_id,

        ))

    def change_password(self, user_id, password):

        self.execute("""
            UPDATE users
            SET password = ?
            WHERE id = ?
        """, (

            password,

            user_id,

        ))

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(self, user_id):

        self.execute("""
            DELETE FROM users
            WHERE id = ?
        """, (user_id,))


user_repository = UserRepository()