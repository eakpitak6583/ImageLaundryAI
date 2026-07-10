"""
Image Laundry AI
User Model
"""

from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, user):

        # รองรับ sqlite3.Row
        if hasattr(user, "keys"):

            self.id = user["id"]
            self.username = user["username"]
            self.fullname = user.get("fullname") if hasattr(user, "get") else user["fullname"]

            try:
                self.email = user["email"]
            except Exception:
                self.email = ""

            try:
                self.role = user["role"]
            except Exception:
                self.role = "user"

            try:
                self.active = bool(user["active"])
            except Exception:
                self.active = True

        # รองรับ dict
        elif isinstance(user, dict):

            self.id = user.get("id")
            self.username = user.get("username")
            self.fullname = user.get("fullname", "")
            self.email = user.get("email", "")
            self.role = user.get("role", "user")
            self.active = user.get("active", True)

        else:

            raise TypeError("Invalid user object")

    def get_id(self):

        return str(self.id)

    @property
    def is_active(self):

        return bool(self.active)

    @property
    def is_authenticated(self):

        return True

    @property
    def is_anonymous(self):

        return False