from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Book
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        book = request.form.get('book')

        if len(book) < 1:
            flash('Book is too short!', category='error') 
        else:
            new_book = Book(data=book, user_id=current_user.id)  
            db.session.add(new_book) 
            db.session.commit()
            flash('Book added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-book', methods=['POST'])
def delete_book():  
    book = json.loads(request.data) 
    bookId = book['bookId']
    book = Book.query.get(bookId)
    if book:
        if book.user_id == current_user.id:
            db.session.delete(book)
            db.session.commit()

    return jsonify({})