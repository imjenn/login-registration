from flask import Flask, render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
import re

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

r_p = re.compile('^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])')

@app.route('/')
def index():
    all_users = User.get_all()
    return render_template("index.html", all_users=all_users)

# Action route
@app.route('/register', methods=['POST'])
def register():
    # Validate first
    user_dict = request.form.to_dict()
    if not User.is_valid(request.form):
        return redirect('/')

    if not r_p.match(user_dict['pw1']):
        flash("Password be at least 6 characters, include a digit number, and at least an uppercase and lowercase letter.")
        return redirect('/')

    # Bcrypt
    pw_hash = bcrypt.generate_password_hash(request.form['pw1'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    
    user_id = User.create(data)
    print(user_id)
    session['user_id'] = user_id
    return redirect("/dashboard")

@app.route('/login', methods=['POST'])
def login():
    user_in_db = User.get_by_email(request.form)

    # if user is not in db
    if not user_in_db:
        flash("Invalid email/password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # If we get false after checking the pw
        flash("Invalid email/password")
        return redirect("/")
    # if pws matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    return redirect("/dashboard")

# User page after successful login
@app.route('/dashboard')
def display():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : session['user_id']
    }
    return render_template("dashboard.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

# If user enter in any other path
# @app.route("/", defaults=['path': ''])
# @app.route('/<path:path>')
# def catch_all(path):
#     return 'Error 404 page not found'