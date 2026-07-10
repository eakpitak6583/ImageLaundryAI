"""
LaundryBot V7 Enterprise
Authentication Service
"""

import bcrypt

from flask_login import UserMixin
from werkzeug.security import check_password_hash

from repositories import user_repository


# ==========================================================
# User Model
# ==========================================================

class User(UserMixin):

    def __init__(self, row):

        self.id = row["id"]

        self.username = row["username"]

        self.fullname = row["fullname"] or ""

        self.role = row["role"] or "user"

    @property
    def is_active(self):

        return True


# ==========================================================
# Authentication
# ==========================================================

class AuthService:

    def login(self, username, password):

        user = user_repository.login(username)

        if user is None:
            return None

        stored = user["password"]

        # --------------------------------------------------
        # BCrypt
        # --------------------------------------------------

        if stored.startswith("$2"):

            if not bcrypt.checkpw(

                password.encode(),

                stored.encode()

            ):

                return None

        # --------------------------------------------------
        # Werkzeug
        # --------------------------------------------------

        elif stored.startswith(("pbkdf2:", "scrypt:")):

            if not check_password_hash(

                stored,

                password

            ):

                return None

        # --------------------------------------------------
        # Plain Text
        # --------------------------------------------------

        else:

            if stored != password:

                return None

        return User(user)

    def logout(self):

        return True

    def current_user(self, user_id):

        return load_user(user_id)


# ==========================================================
# Flask Login
# ==========================================================

def load_user(user_id):

    row = user_repository.get(int(user_id))

    if row is None:

        return None

    return User(row)


auth_service = AuthService()