from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from .models import User, Book, Review, Like, List
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

@views.route('/', methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        return render_template('h.html')
    if request.method == 'POST':
        book_id = request.form.get('book_id')
        if book_id:
            book = Book.query.filter_by(id=book_id).first()
            if book and book not in current_user.books:
                current_user.books.append(book)
                db.session.commit()
        return redirect(url_for('views.index'))
    
    reviews = []
    for book in current_user.books:
        book_reviews = Review.query.filter(Review.book_isbn==book.isbn, Review.user_email!=current_user.email).all()
        reviews.extend(book_reviews)

    book_titles = {}
    for review in reviews:
        book = Book.query.filter_by(isbn=review.book_isbn).first()
        if book:
            book_titles[review.book_isbn] = book.title

    user_list = db.session.query(Book, List.is_read)\
        .join(List, (List.book_id == Book.id))\
        .filter(List.user_id == current_user.id)\
        .all()
    list = [{'book': book, 'is_read': is_read} for book, is_read in user_list]
    
    books = Book.query.order_by(Book.title).all()
    return render_template('index.html', user=current_user, books=books, reviews=reviews, book_titles=book_titles, lists=list)

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
            return redirect(request.referrer)
        return render_template('edit_review.html', review=review)
    else:
        flash('No tienes permiso para editar esta review.', category='error')
        return redirect(url_for('views.index'))

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
    return redirect(request.referrer)

@views.route('/get_suggestions', methods=['GET', 'POST'])
def get_suggestions():
    input = request.form.get('input')
    suggestions = Book.query.filter(Book.title.ilike('%' + input + '%')).all()
    return jsonify([{'title': book.title, 'id': book.id} for book in suggestions])



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
        book = List.query.filter_by(book_id=book_id, user_id=current_user.id).first()
        if book:
            book.is_read = not book.is_read
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

@views.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        new_first_name = request.form.get('new_first_name')
        new_email = request.form.get('new_email')
        
        # Perform server-side validation
        if not new_first_name or len(new_first_name) > 50:
            flash('Invalid first name.', category='error')
            return redirect(url_for('views.edit_profile'))

        if not new_email or len(new_email) > 50 or '@' not in new_email:
            flash('Invalid email.', category='error')
            return redirect(url_for('views.edit_profile'))

        # Check if the new email is already in use
        existing_user = User.query.filter(User.email == new_email, User.id != current_user.id).first()
        if existing_user:
            flash('Email already in use.', category='error')
            return redirect(url_for('views.edit_profile'))

        # Update user information
        current_user.first_name = new_first_name
        current_user.email = new_email
        db.session.commit()

        flash('Your profile has been updated!', category='success')
        return redirect(url_for('views.edit_profile'))

    return render_template("edit_profile.html", user=current_user)





@views.route('/search', methods=['GET'])
def search_user():
    query = request.args.get('query', '')
    if not query == "":
        user = User.query.filter(User.first_name.contains(query)).first()
        if user:
            
            return redirect(url_for('views.user_profile', user_id=user.id))
    else:
        flash('No existe usuario con ese nombre.', category='error')
        return redirect(url_for('views.index'))
    
  
@views.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def user_profile(user_id):
    user = User.query.get(user_id)
    if user:
        if request.method == 'POST':
            book_id = request.form.get('book_id')
            if book_id:
                book = Book.query.filter_by(id=book_id).first()
                if book and book not in user.books:
                    user.books.append(book)
                    db.session.commit()
            return redirect(url_for('views.user_profile', user_id=user.id))
        
        # Obtener las reseñas del usuario
        reviews = Review.query.filter_by(user_email=user.email).all()
        
        # Crear un diccionario para almacenar los títulos de los libros
        book_titles = {}
        for review in reviews:
            book = Book.query.filter_by(isbn=review.book_isbn).first()
            if book:
                book_titles[review.book_isbn] = book.title
        
        books = Book.query.all()
        return render_template('profile.html', user=user, books=books, reviews=reviews, book_titles=book_titles)
    else:
        # Usuario no existe
        return redirect(url_for('views.index'))
    



