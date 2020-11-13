import bcrypt

from models.base import BaseModel
from core.database import db


class User(db.Model, BaseModel):
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, index=True, nullable=False)
    _password = db.Column(db.String(128), nullable=False)

    def __init__(self, name, email, password, **kwargs):
        super(User, self).__init__(**kwargs)
        """ Create a new User """
        self.name = name
        self.email = email
        self._password = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()).decode()

    def __repr__(self):
        return "User::{}".format(self.id)

    def check_password(self, password: str):
        return bcrypt.checkpw(password=password.encode(), hashed_password=self._password.encode())
