from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import pandas as pd

user_books = db.Table('user_books',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(150), unique=True)
    title = db.Column(db.String(500))
    author = db.Column(db.String(300))
    year = db.Column(db.Integer)
    alreadyRead = db.Column(db.Boolean, default=False)

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
    profile_picture = db.Column(db.String(20), nullable=False, default='default.jpg')
    notes = db.relationship('Note')
    books = db.relationship('Book', secondary=user_books, backref=db.backref('users', lazy='dynamic'))  # New relationship

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_isbn = db.Column(db.String(150), db.ForeignKey('book.isbn'))
    user_email = db.Column(db.String(150), db.ForeignKey('user.email'))
    review = db.Column(db.String(5000))
    rating = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    likes = db.relationship('Like', backref='review', lazy='dynamic')

class Like(db.Model):
    __tablename__ = 'likes'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), primary_key=True)