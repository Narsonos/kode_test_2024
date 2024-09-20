from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import json


db = SQLAlchemy()


#User class implementation
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True)
    password_hash = db.Column(db.String())
    notes = relationship("Note", backref='owner',lazy='dynamic')

    def set_password(self, password: str) -> None:
        self.password_hash: str = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username: str) -> 'User | None':
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_id(id: int) -> 'User | None':
        return User.query.get(int(id))

    def __repr__(self) -> str:
        return f"User {self.username}"


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    content = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)

    def to_dict(self) -> dict:
        return dict(id=self.id,name=self.name,content=self.content,owner_id=self.owner_id)