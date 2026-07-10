from dataclasses import dataclass
from flask_login import UserMixin


@dataclass
class User(UserMixin):

    id: int
    username: str
    fullname: str
    email: str
    role: str
    active: int

    def get_id(self):
        return str(self.id)