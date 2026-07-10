"""
Image Laundry AI
Authentication Service
"""

from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from repositories.user_repository import (
    user_repository,
)


class AuthService:

    # ==========================================================
    # Login
    # ==========================================================

    def login(self, username, password):

        user = user_repository.login(username)

        if not user:
            return None

        db_password = user["password"]

        # รองรับทั้ง Password แบบ Hash และ Plain Text
        try:

            if db_password.startswith(("pbkdf2:", "scrypt:")):

                if not check_password_hash(
                    db_password,
                    password,
                ):
                    return None

            else:

                if db_password != password:
                    return None

        except Exception:

            if db_password != password:
                return None

        return user

    # ==========================================================
    # Create User
    # ==========================================================

    def create_user(self, data):

        data = dict(data)

        data["password"] = generate_password_hash(
            data["password"]
        )

        return user_repository.create(data)

    # ==========================================================
    # Change Password
    # ==========================================================

    def change_password(

        self,

        user_id,

        new_password,

    ):

        password = generate_password_hash(
            new_password
        )

        user_repository.change_password(

            user_id,

            password,

        )

    # ==========================================================
    # Get
    # ==========================================================

    def get(self, user_id):

        return user_repository.get(user_id)

    def get_all(self):

        return user_repository.get_all()

    # ==========================================================
    # Update
    # ==========================================================

    def update(self, user_id, data):

        user_repository.update(

            user_id,

            data,

        )

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(self, user_id):

        user_repository.delete(user_id)


auth_service = AuthService()
# ==========================================================
# Flask-Login
# ==========================================================

from repositories.user_repository import user_repository
from models.user import User


def load_user(user_id):

    user = user_repository.get(int(user_id))

    if not user:
        return None

    return User(user)