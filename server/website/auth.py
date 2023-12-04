from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   
from flask_login import login_user, login_required, logout_user, current_user
import os
import uuid
from flask import current_app as app
from werkzeug.utils import secure_filename


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.index'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        user = current_user
        name = request.form.get('new_first_name')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        new_password_confirmation = request.form.get('new_password_confirmation')

        if user:
            if name:
                user.first_name = name
            if 'picture' in request.files:
                picture = request.files['picture']
                if picture.filename != '' and '.' in picture.filename and picture.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
                    filename = str(uuid.uuid4()) + secure_filename(picture.filename)
                    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    picture.save(path)
                    print("HEEEEEEEEEELP")
                    print(path)
                    user.photo_path = path
            if new_password and new_password_confirmation:
                if not check_password_hash(user.password, current_password):
                    flash('Incorrect current password.', category='error')
                    return redirect(url_for('auth.edit_profile'))
                if new_password != new_password_confirmation:
                    flash('New passwords don\'t match.', category='error')
                    return redirect(url_for('auth.edit_profile'))
                elif len(new_password) < 7:
                    flash('New password must be at least 7 characters.', category='error')
                    return redirect(url_for('auth.edit_profile'))
                else:
                    user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
            db.session.commit()
            flash('Profile updated!', category='success')
            return redirect(url_for('auth.profile'))
    return render_template("profile.html", user=current_user)

@auth.route('/profile/edit')
@login_required
def edit_profile():
    return render_template("edit_profile.html", user=current_user)

@auth.route('/idlibro', methods=['GET', 'POST'])
@login_required
def idlibro():
    return render_template("profile.html", user=current_user)
