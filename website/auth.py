from flask import Blueprint, render_template, request, flash, redirect
from flask.helpers import url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('logged in ', category='success')
                login_user(user, remember=True)
                redirect(url_for('views.home'))
            else:
                flash('incorrect password', category='error')
        else:
            flash('email does not exist', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        user = User.query.filter_by(email=email)
        if user:
            flash('user already exists', category='error')

        if len(email) < 4:
            flash("Email must be greater than 4 chars", category='error')
        elif len(name) < 2:
            flash('Name is too short', category='error')
        elif len(password) < 6:
            flash('Password is too short', category='error')
        else:
            # add the user
            new_user = User(email=email, name=name, password=generate_password_hash(
                password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully", category='success')
            # blueprint name . function name
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)
