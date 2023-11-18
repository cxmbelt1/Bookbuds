import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
	command1 ="""\n
/*  --------------------------------------------------------\n
                   SQL Execution \n
    -------------------------------------------------------- */"""
	print(command1)
	print("/*  ---------------------------Create Table users-----------------------------*/")

	#create table users
	db.execute("""CREATE TABLE users(
    				id serial primary key,
    				username text unique NOT NULL,
    				hash text NOT NULL)""")

	print("table users created\n")

	print("/*  ---------------------------Create Table books-----------------------------*/")

	#create table books
	db.execute("""CREATE TABLE books(
				    id serial primary key,
				    isbn char(10) unique NOT NULL,
				    title text NOT NULL,
				    author text NOT NULL,
				    year char(4) NOT NULL)""")

	print("table books created\n")

	print("/*  ---------------------------Create Table reviews-----------------------------*/")

	#create table reviews
	db.execute("""CREATE TABLE reviews(
				    id serial primary key,
				    user_name text references users(username),
				    book_id integer references books(id),
				    rating integer NOT NULL ,
				    comment varchar(1500) NOT NULL,
				    timezone timestamptz)""")

	print("table reviews created\n")

	#insert datas from csv file to books table
	print("/*  ---------------------------Insert into Table books-----------------------------*/\n\n")
	print("fetching datas from books.csv")

	f = open("books.csv")
	reader = csv.reader(f)
	count = 0

	for isbn, title, author,year in reader:
		if not isbn=="isbn":
			count += 1
			db.execute("INSERT INTO books (isbn, title, author,year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year":year})
			print(f"added book {title}, by {author}, in {year}; {isbn}")
			print(f"1 ROW affected")


	print(f" {count} rows inserted!")
	print(f"books added successfully")
	db.commit()
    	 		 
if __name__ == "__main__":
    main()
