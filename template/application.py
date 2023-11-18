import os, json

from flask import Flask, session, redirect, render_template,url_for, request, jsonify, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from werkzeug.security import check_password_hash, generate_password_hash
from math import *
import requests
import datetime
import pytz

from login_function import login_required

app = Flask(__name__)
app.secret_key='dont tell anyone'

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    
    # clear every session of users
    session.clear()

    username = request.form.get("username")

    # when press the submit button, via post 
    if request.method == "POST":

        # input request validation for user
        if not request.form.get("username"):
            return render_template("signin.html", error="must provide username")

        # input request validation for password
        elif not request.form.get("password"):
            return render_template("signin.html", error="must provide password")

       
        # query to access user
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                            {"username": username})
        
        result = rows.fetchone()

        # Authentication
        if result == None or not check_password_hash(result[2], request.form.get("password")):
            return render_template("signin.html", error="invalid username and/or password")

        # assign session for saving user details as a session
        session["user_id"] = result[0]
        session["user_name"] = result[1]
        success ="Welcome " + session["user_name"]+"!"


        # Redirect user to home page
        flash(success)
        return redirect("/search")

    # To prevent access from unknown people via get method or any else
    else:
        return render_template("signin.html")

@app.route("/logout")
def logout():
    """ Log user out """

    # session cleared
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register user """
    
    # Session cleared
    session.clear()
    
    #when press the submit button, via post 
    if request.method == "POST":

        # input request validation for username
        if not request.form.get("username"):
            return render_template("register.html", error="must provide username")

        # Check if username is already exist
        userCheck = db.execute("SELECT * FROM users WHERE username = :username",
                          {"username":request.form.get("username")}).fetchone()

        # Check if username already exist
        if userCheck:
            return render_template("register.html", error="username already exist")

        # input request validation for password
        elif not request.form.get("password"):
            return render_template("register.html", error="must provide password")

        # input request validation for confirmation 
        elif not request.form.get("confirmation"):
            return render_template("register.html", error="must confirm password")

        # Check passwords are equal
        elif not request.form.get("password") == request.form.get("confirmation"):
            return render_template("register.html", error="password shouldn\'t match")
        

        # Hash user's password to store in DB
        hashedPassword = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        
        # Insert register into DB
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)",
                            {"username":request.form.get("username"), 
                             "password":hashedPassword})

        # Commit changes to database
        db.commit()

        # Redirect user to login page
        return render_template("success.html", success="Thank you for being our customer")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/search")
@login_required
def search():
    return render_template("search.html")

@app.route("/book", methods=["GET", "POST"])
@login_required
def book():
    if request.method == "POST":
        """ Get books results """

    # Check book id was provided
    if not request.form.get("book"):
        return render_template("book.html", error="Sorry! make sure that keywords are spelled correctly")

    # Take input and add a wildcard
    query = "%" + request.form.get("book") + "%"

    # Capitalize all words of input for search
    query = query.title()
    
    rows = db.execute("SELECT id,isbn, title, author, year FROM books WHERE \
                        isbn LIKE :query OR \
                        title LIKE :query OR \
                        author LIKE :query ORDER BY id DESC",
                        {"query": query})

    ''' rows = db.execute("SELECT id,isbn, title, author, year FROM books WHERE \
                        isbn LIKE :query OR \
                        title LIKE :query OR \
                        author LIKE :query ORDER BY id DESC LIMIT 18",
                        {"query": query})
    '''

    count=rows.rowcount
    # Books not founded
    if rows.rowcount == 0:
        return render_template("book.html",error="Sorry! No Result found!!")
    
    # Fetch all the results
    books = rows.fetchall()

    # Creates a list containing total 'count' lists, each of '2' items, all set to 0
    rate = [[0 for x in range(2)] for y in range(count)]
    
    # Read API key from env variable
    key = os.getenv("GOODREADS_KEY")
    
        
    for i in range(count):
        for j in range(2):
            isbn = books[i][1]

            res = requests.get("https://www.goodreads.com/book/review_counts.json",
                params={"key": key, "isbns": isbn})

            response = res.json()

            # "Clean" the JSON before passing it to the bookInfo list
            average_rating = response['books'][0]['average_rating']
            average_rating = float(average_rating)
            average_rating = floor(average_rating)

            rate[i][0] = isbn
            rate[i][1] = average_rating

    return render_template("book.html", books=books, rate=rate, count=count)
    


@app.route("/book/<isbn>", methods=['GET','POST'])
@login_required
def bookDeatails(isbn):

    if request.method == "POST":
        
        # Save current user info
        currentUser = session["user_name"]
        
        # Fetch form data of comment
        rating = int(request.form["rating"])
        comment = request.form.get("comment")

        #validate rating input is filled
        if rating == 0:
            flash(u'Please rate this book!', 'error');
            return redirect("/book/" + isbn)

        #validate comment input is filled
        elif not request.form.get("comment"):
            flash(u'Leave Us a review!', 'error');
            return redirect("/book/" + isbn)
        
        # Search book_id by ISBN
        row = db.execute("SELECT id FROM books WHERE isbn = :isbn",
                        {"isbn": isbn})

        # Save id into variable
        bookId = row.fetchone() 
        bookId = bookId[0]

        # set allocation to each users for sharing reviews as only one
        row2 = db.execute("SELECT * FROM reviews WHERE user_name = :user_name AND book_id = :book_id",
                    {"user_name": currentUser,
                     "book_id": bookId})

        # A review already exists
        if row2.rowcount == 1:
            flash(u'Sorry! You already submitted a review for this book!', 'error');
            return redirect("/book/" + isbn)

        #take date and time from system with timezone 00:00
        dt_utc = datetime.datetime.now(tz=pytz.UTC)

        #set timezone to India as 'Asia/Calcutta' ,which means set timezone to +05:30
        dt_ind = dt_utc.astimezone(pytz.timezone('Asia/Calcutta') )


        # strftime - Datetime to String
        # dt_to_string = dt_ind.strftime('%b %d, %Y') 
        # strptime - String to Datetime
        # string_to_dt = datetime.datetime.strptime(dt_to_string, '%b %d, %Y')

        db.execute("INSERT INTO reviews (user_name, book_id, comment, rating ,timezone) VALUES \
                    (:user_name, :book_id, :comment, :rating ,:timezone)",
                    {"user_name": currentUser, 
                    "book_id": bookId, 
                    "comment": comment, 
                    "rating": rating,
                    "timezone":dt_ind})

        # Commit transactions to DB and close the connection
        db.commit()

        flash(u'Thank you for participating in our survey!', 'success');
        return redirect("/book/" + isbn)
    
    # Take the book ISBN and redirect to his page (GET)
    else:

        row = db.execute("SELECT isbn, title, author, year FROM books WHERE \
                        isbn = :isbn",
                        {"isbn": isbn})

        bookInfo = row.fetchall()

        # GOODREADS reviews

        # Read API key from env variable
        key = os.getenv("GOODREADS_KEY")
        
        # Query the api with key and ISBN as parameters
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                params={"key": key, "isbns": isbn})

        # Convert the response to JSON
        response = res.json()

        #take parameter average rating
        average_rating = response['books'][0]['average_rating']  # access the average rating from goodreads api
        
        average_rating = float(average_rating) #convert parameter average rating to float type

        average_rating = round(average_rating,2) #rounded decimal value of parameter average rating only 2 digits

        average_rating1= floor(average_rating)  #return closest integer less than actual value for starring purpose

        
        total_rating = response['books'][0]['work_ratings_count']  #access the parameter total rating from goodreads api

        total_rating = int(total_rating) #convert the parameter total rating into an integer type

        total_rating = "{:,}".format(total_rating)  #  integer in international place value format and put commas at the appropriate place, from the right.

        
        """ Users reviews """

         # Search book_id by ISBN
        row = db.execute("SELECT id FROM books WHERE isbn = :isbn",
                        {"isbn": isbn})

        # Save id into variable
        book = row.fetchone() # (id,)
        book = book[0]

        # Fetch book reviews
        # Date formatting (https://www.postgresql.org/docs/9.1/functions-formatting.html)
        results = db.execute("SELECT user_name, comment, rating, to_char(timezone, 'Mon DD, YYYY') as times\
                                FROM reviews WHERE book_id = :book ORDER BY id DESC",
                                {"book": book})

        reviews = results.fetchall()

        return render_template("review.html", bookInfo=bookInfo, reviews=reviews , 
                                average_rating=average_rating ,average_rating1=average_rating1 ,  total_rating= total_rating)


@app.route("/api/<isbn>",methods=['GET'])
@login_required
def api_call(isbn):

    # COUNT returns rowcount
    # SUM returns sum selected cells' values
    # INNER JOIN associates books with reviews tables

    row = db.execute("SELECT isbn, title, author, year FROM books WHERE \
                        isbn = :isbn",
                        {"isbn": isbn})
    if row.rowcount == 0:
        return render_template("404.html")

    review = row.fetchone()

    key = os.getenv("GOODREADS_KEY")
        
    # Query the api with key and ISBN as parameters
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                params={"key": key, "isbns": isbn})
    # Convert the response to JSON
    response = res.json()
    average_rating = response['books'][0]['average_rating']
    total_rating = response['books'][0]['work_ratings_count']

    dict = {
            "title":review.title,
            "author":review.author,
            "year":review.year,
            "isbn":review.isbn,
            "review_count":total_rating,
            "average_score":average_rating
    }

    return jsonify(dict)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#initialise and change debug to 1
if __name__ == '__main__':
    app.run(debug=True)

