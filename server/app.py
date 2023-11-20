from Untitled1 import Storage
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/dashboard")
def dashboard():
    
    books_df = pd.read_csv('books.csv', on_bad_lines='skip')
    book_titles = books_df['title'].head(3).tolist()  
    
    return render_template("dashboard.html", book_titles=book_titles)

@app.route("/search")
def search():
    query = request.args.get('query', '')  
    storage = Storage()
    search_results = storage.search_books(query)  
    return render_template("search_results.html", books=search_results, query=query)

if __name__ == '__main__':
    app.run(debug=True)

