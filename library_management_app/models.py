from library_management_app.extensions import db


class Book(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(100), nullable=False)
    author: str = db.Column(db.String(100), nullable=False)


class Member(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(50), unique=True, nullable=False)
    password: str = db.Column(db.String(100), nullable=False)  #
