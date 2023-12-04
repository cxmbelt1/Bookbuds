from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import pandas as pd

class HashSet:
    def __init__(self):
        self.table = {}

    def add(self, item):
        self.table[item] = True

    def remove(self, item):
        if item in self.table:
            del self.table[item]

    def contains(self, item):
        return item in self.table
    
class HashMap:
    def __init__(self):
        self.table = {}

    def set(self, key, value):
        self.table[key] = value

    def get(self, key):
        return self.table.get(key, None)

    def remove(self, key):
        if key in self.table:
            del self.table[key]

class HashGraph:
    def __init__(self):
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, vertex1, vertex2):
        self.adjacency_list[vertex1].append(vertex2)
        self.adjacency_list[vertex2].append(vertex1)

class HashCounter:
    def __init__(self):
        self.counts = {}

    def add(self, item):
        if item in self.counts:
            self.counts[item] += 1
        else:
            self.counts[item] = 1

    def get_count(self, item):
        return self.counts.get(item, 0)
    
class HashCache:
    def __init__(self):
        self.cache = {}

    def set(self, key, value):
        self.cache[key] = value

    def get(self, key):
        return self.cache.get(key, None)
    
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(150), unique=True)
    title = db.Column(db.String(500))
    author = db.Column(db.String(300))
    year = db.Column(db.Integer)
    users = db.relationship('User', secondary='list')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'user_id': self.user_id
        }

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class List(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    is_read = db.Column(db.Boolean, default=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    books = db.relationship('Book', secondary='list')
    reviews = db.relationship('Review')
    photo_path = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'books': [book.to_dict() for book in self.books]
        }

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_isbn = db.Column(db.String(150), db.ForeignKey('book.isbn'))
    user_email = db.Column(db.String(150), db.ForeignKey('user.email'))
    review = db.Column(db.String(5000))
    rating = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    likes = db.relationship('Like', backref='review', lazy='dynamic')
    user = db.relationship('User', backref='review')

    def to_dict(self):
        return {
            'id': self.id,
            'book': self.bookisbn,
            'review': self.revieww,
            'author': self.author,
            'user_id': self.user_id
        }

class Like(db.Model):
    __tablename__ = 'likes'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), primary_key=True)
