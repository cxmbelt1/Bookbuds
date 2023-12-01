from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from .models import User
from . import db
import json
from flask import redirect, url_for

views = Blueprint('views', __name__)


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