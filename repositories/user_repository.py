"""
LaundryBot V7 Enterprise
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
        ใช้สำหรับ Authentication
        การตรวจสอบ Password ทำใน AuthService
        """
        return self.fetch_one("""
            SELECT *
            FROM users
            WHERE username = ?
              AND active = 1
        """, (username,))

    def get_active_users(self):
        return self.fetch_all("""
            SELECT *
            FROM users
            WHERE active = 1
            ORDER BY fullname
        """)

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
            email,
            role,
            active
        )
        VALUES
        (
            ?, ?, ?, ?, ?, ?
        )
        """

        return self.execute(sql, (
            data["username"],
            data["password"],
            data.get("fullname"),
            data.get("email"),
            data.get("role", "technician"),
            data.get("active", 1)
        ))

    # ==========================================================
    # Update
    # ==========================================================

    def update(self, user_id, data):

        sql = """
        UPDATE users
        SET
            fullname = ?,
            email = ?,
            role = ?,
            active = ?
        WHERE id = ?
        """

        self.execute(sql, (
            data.get("fullname"),
            data.get("email"),
            data.get("role"),
            data.get("active", 1),
            user_id
        ))

    def change_password(self, user_id, password):

        self.execute("""
            UPDATE users
            SET password = ?
            WHERE id = ?
        """, (
            password,
            user_id
        ))

    # ==========================================================
    # Delete (Soft Delete)
    # ==========================================================

    def deactivate(self, user_id):

        self.execute("""
            UPDATE users
            SET active = 0
            WHERE id = ?
        """, (user_id,))

    def activate(self, user_id):

        self.execute("""
            UPDATE users
            SET active = 1
            WHERE id = ?
        """, (user_id,))

    def delete(self, user_id):

        self.execute("""
            DELETE FROM users
            WHERE id = ?
        """, (user_id,))


user_repository = UserRepository()