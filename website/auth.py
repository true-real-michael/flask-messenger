from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from .database import models

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    email = ''
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # user = User.query.filter_by(email=email).first()
        user = models.find_user_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            flash('logged in successfully', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            flash('invalid email or password', category='error')

    return render_template('login.html', email=email, user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    email = name = ''
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = models.find_user_by_email(email)
        if user:
            flash('user with this email already exists', category='error')
        elif len(email) < 4:
            flash('email must be at least 4 charachters', category='error')
        elif len(password1) < 1:
            flash('password cannot be empty', category='error')
        elif password1 != password2:
            flash('passwords do not match', category='error')
        else:
            new_user = models.create_user(email, generate_password_hash(password1, method='sha256'), name)
            flash('account created', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template('signup.html', email=email, name=name, user=current_user)
