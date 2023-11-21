from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Colum(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezon=True,default=func.now()))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))



class User(db.Model, UserMixin):
    id = db.Colum(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Colummn(db.String(150))
    notes = db.relationship('Note')