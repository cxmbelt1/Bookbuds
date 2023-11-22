from flask import Blueprint

views = Blueprint("views", __name__)

@views.route("/home")
def home():
    return "<h1>Cachon</h1>"