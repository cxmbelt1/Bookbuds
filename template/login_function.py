from flask import redirect, render_template, request, session
from functools import wraps

def login_required(f):
    
    #Check Logged in by using session
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function