from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from .models import User, Book, Review, Like
from . import db
import json
from flask import redirect, url_for
from sqlalchemy import desc, func
import requests
import json


views = Blueprint('views', __name__)

def get_book_cover(isbn):
    return f'https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg'

from sqlalchemy import func, desc

@views.route('/book/<isbn>', defaults={'sort': 'likes', 'order': 'desc'}, methods=['GET', 'POST'])
@views.route('/book/<isbn>/<sort>', defaults={'order': 'desc'}, methods=['GET', 'POST'])
@views.route('/book/<isbn>/<sort>/<order>', methods=['GET', 'POST'])
@login_required
def book(isbn, sort, order):
    book = Book.query.filter_by(isbn=isbn).first_or_404()
    cover_url = get_book_cover(isbn)  

    reviewed = False
    invalid_feedback = False

    if request.method == "POST":
        review = request.form.get("review")
        rating = request.form.get("rating")

        if review == "" or rating is None:
            invalid_feedback = "Todos los campos son requeridos."
            pass
       
        elif Review.query.filter_by(book_isbn=isbn, user_email=current_user.email).first():
            reviewed = "Ya hiciste una review para este libro :p ."

        else:
            new_review = Review(book_isbn=book.isbn, user_email=current_user.email, review=review, rating=rating)
            db.session.add(new_review)
            db.session.commit()

    if sort == 'likes':
        if order == 'asc':
            reviews = Review.query.filter_by(book_isbn=book.isbn).outerjoin(Like).group_by(Review.id).order_by(func.count(Like.user_id).asc()).all()
        else:
            reviews = Review.query.filter_by(book_isbn=book.isbn).outerjoin(Like).group_by(Review.id).order_by(func.count(Like.user_id).desc()).all()
    elif sort == 'date':
        if order == 'asc':
            reviews = Review.query.filter_by(book_isbn=book.isbn).order_by(Review.date.asc()).all()
        else:
            reviews = Review.query.filter_by(book_isbn=book.isbn).order_by(desc(Review.date)).all()
    elif sort == 'length':
        if order == 'asc':
            reviews = Review.query.filter_by(book_isbn=book.isbn).order_by(func.length(Review.review).asc()).all()
        else:
            reviews = Review.query.filter_by(book_isbn=book.isbn).order_by(func.length(Review.review).desc()).all()
    else:
        reviews = Review.query.filter_by(book_isbn=book.isbn).all()

    return render_template('book.html', book=book, user=current_user, reviews=reviews, reviewed=reviewed, invalid_feedback=invalid_feedback, cover_url=cover_url)


@views.route('/edit_review/<int:review_id>', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    review = Review.query.get(review_id)
    if review and review.user_email == current_user.email:
        if request.method == 'POST':
            new_review_text = request.form.get('review')
            new_rating = request.form.get('rating')
            if new_review_text and new_rating:
                review.review = new_review_text
                review.rating = new_rating
                db.session.commit()
                flash('Tu reseña ha sido actualizada!', category='success')
            else:
                flash('Completa todos los campos!', category='error')
            return redirect(url_for('views.book', isbn=review.book_isbn))
        return render_template('edit_review.html', review=review)
    else:
        flash('No tienes permiso para editar esta review.', category='error')
        return redirect(url_for('views.home'))

@views.route('/review/<int:review_id>/like', methods=['POST'])
@login_required
def like_review(review_id):
    review = Review.query.get_or_404(review_id)
    like = Like.query.filter_by(user_id=current_user.id, review_id=review.id).first()
    if like is None:
        like = Like(user_id=current_user.id, review_id=review.id)
        db.session.add(like)
    else:
        db.session.delete(like)
    db.session.commit()
    return redirect(url_for('views.book', isbn=review.book_isbn))


@views.route('/delete_review/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get(review_id)
    if review and review.user_email == current_user.email:
        Like.query.filter_by(review_id=review.id).delete()
        db.session.delete(review)
        db.session.commit()
    return redirect(url_for('views.book', isbn=review.book_isbn))

@views.route('/get_suggestions', methods=['GET', 'POST'])
def get_suggestions():
    input = request.form.get('input')
    suggestions = Book.query.filter(Book.title.ilike('%' + input + '%')).all()
    return jsonify([{'title': book.title, 'id': book.id} for book in suggestions])

@views.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        book_id = request.form.get('book_id')
        if book_id:
            book = Book.query.filter_by(id=book_id).first()
            if book and book not in current_user.books:
                current_user.books.append(book)
                db.session.commit()
        return redirect(url_for('views.index'))
    books = Book.query.all()
    return render_template('index.html', user=current_user, books=books)


@views.route('/delete_book', methods=['POST'])
@login_required
def delete_book():
    book_id = request.form.get('book_id')
    if book_id:
        book = Book.query.filter_by(id=book_id).first()
        if book and book in current_user.books:
            current_user.books.remove(book)
            db.session.commit()
    return redirect(url_for('views.index'))

@views.route('/toggle_read', methods=['POST'])
@login_required
def toggle_read():
    book_id = request.form.get('book_id')
    if book_id:
        book = Book.query.filter_by(id=book_id).first()
        if book and book in current_user.books:
            book.alreadyRead = not book.alreadyRead  # Toggle the 'alreadyRead' status
            db.session.commit()
    return redirect(url_for('views.index'))

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  
            db.session.add(new_note) 
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("home.html", user=current_user)


@views.route('/search', methods=['GET'])
def search_user():
    query = request.args.get('query', '')
    user = User.query.filter(User.first_name.contains(query)).first()
    if user:
        
        return redirect(url_for('views.user_profile', user_id=user.id))
    else:
        
        return redirect(url_for('views.home'))
    
@views.route('/profile/<int:user_id>', methods=['GET'])
def user_profile(user_id):
    user = User.query.get(user_id)
    if user:
        return render_template('profile.html', user=user)
    else:
        #usuario no existe
        return redirect(url_for('views.home'))

@views.route('/home', methods=['GET'])
def bookbuds():
    return render_template('h.html')