from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) 
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Username/Password', category='error')
        else:
            flash('Incorrect Username/Password', category='error')
    return render_template("login.html", user=current_user)

@auth.route("/logout")  
@login_required   
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/sign-up", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        email = request.form.get("email")
        department = request.form.get("department")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")


        #Extra security features
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Department user already exists, please log in.", category="error")
        
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')

        elif "@" not in email:
            flash('Email must contain "@"', category='error')

        elif len(department) < 2:
            flash('Department must be greater than 1 character.', category='error')

        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')

        elif len(password1) < 7:
            flash('Password must be at least 8 characters.', category='error')

        else:
            new_user = User(email=email, department=department, password=generate_password_hash(password1, method="sha256"))
            
            #Add user to the database
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            flash('Account Successfully Created!', category='success')

            return redirect(url_for('views.home'))


    return render_template("signup.html", user=current_user)
