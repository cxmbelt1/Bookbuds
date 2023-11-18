# CS50’s Web Programming with Python and JavaScript
## CS50W Project 1: Books 
#### for more info [course | CS50W | edx](https://courses.edx.org/courses/course-v1:HarvardX+CS50W+Web/course/)

#### Use the app on [Heroku](https://web-development-python-js.herokuapp.com/)
#### Watch on   <img src="https://i.pinimg.com/originals/31/23/9a/31239a2f70e4f8e4e3263fafb00ace1c.png" width="20" height="20" valign="middle"> [Youtube](https://www.youtube.com/watch?v=-cvByPFkQDc)

#### Objective
* Become more comfortable with Python.
* Gain experience with Flask.
* Learn to use SQL to interact with databases

#### Overview

* Users will be able to register and then log in using their username and password. 
* They will be able to search for books, leave reviews for individual books, and see the reviews made by other people. 
* use the a third-party API by **[Goodreads](https://www.goodreads.com/api)**, another book review website, to pull in ratings from a broader audience. 
* Finally, users will be able to query for book details and book reviews programmatically via your website’s API.

#### Requirements
* SQL (PostgreSQL)
  * <img src="https://www.postgresql.org/media/img/about/press/elephant.png" width="20" height="20" valign="middle"> [PostgreSQL](https://www.postgresql.org/download/) (Locally)
  * <img src="https://dab1nmslvvntp.cloudfront.net/wp-content/uploads/2016/04/1461122387heroku-logo.jpg" width="22" height="25" valign="middle"> [Heroku](https://www.heroku.com/) (Online web hosting service)
    * <img src="https://jay.holtslander.ca/img/svg/skills/adminer-logo.svg" width="42" height="29" valign="middle"> [Adminer](https://www.heroku.com/) (for accessing Database)
 * Python and FLask
    * <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/600px-Python-logo-notext.svg.png" width="20" height="20" valign="middle"> [Python](https://www.python.org/downloads/)
    * <img src="https://banner2.cleanpng.com/20190124/rs/kisspng-python-selenium-programming-language-computer-icon-pip-5c4a4a7ca92d33.171618491548372604693.jpg" width="27" height="21" valign="middle"> [pip](https://pip.pypa.io/en/stable/installing/) (install it)

## :gear: CMD Terminal

```cmd
# Navigate into project1 location 
# Git Cloning
> git clone https://github.com/Naufal-AA/cs50-project1.git
#change directory
> cd cs50-project1
>git add . 
>git commit -m "committed"
>git push

# Install necessary packages
> pip3 install -r requirements.txt

# Set the environment variable
> set FLASK_APP = application.py
> set FLASK_DEBUG = 1
> set DATABASE_URL = URL of DATABASE
> set GOODREADS_KEY = Goodreads API Key

#import sql query and insert book details
>python import.py

#run flask
>flask run
```

## DB Schema
![DB](https://i.ibb.co/0tSXJ82/dbschema.png)


# Thank you kindly
* [Goodreads API](https://www.goodreads.com/api)
* [Open Library Covers API](http://covers.openlibrary.org/) (for Collecting Book Cover)
