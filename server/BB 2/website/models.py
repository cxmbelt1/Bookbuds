from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import pandas as pd

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(150), unique=True)
    title = db.Column(db.String(500))
    author = db.Column(db.String(300))
    year = db.Column(db.Integer)
    users = db.relationship('User', secondary='list', backref=db.backref('books', lazy='dynamic'))

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    books = db.relationship('Book', secondary='list', backref=db.backref('users', lazy='dynamic'))

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer, db.ForeingKey('user.id'))

