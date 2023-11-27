from website import create_app
from website import db
from website.models import Book
import pandas as pd
from sqlalchemy.exc import IntegrityError

app = create_app()

with app.app_context():
    books = Book.query.all()

    
    for book in books:
        print(f"ISBN: {book.isbn}, Title: {book.title}, Author: {book.author}, Year: {book.year}")


if __name__ == '__main__':
    app.run(debug=True)
