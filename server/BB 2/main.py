from website import create_app
from website import db
from website.models import Book
import pandas as pd
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text




app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
