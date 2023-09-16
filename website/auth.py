from flask import Blueprint, render_template, request, flash

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    #request = request.form
    return render_template("login.html")

@auth.route("/logout")     
def logout():
    return render_template("login.html", text = "logged out")

@auth.route("/sign-up", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        email = request.form.get("email")
        department = request.form.get("department")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        #Do check ins with the provided info

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        if "@gmail.com" not in email:
            flash('Email must contain "@"', category='error')
        elif len(department) < 2:
            flash('Department must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 8 characters.', category='error')

    else:
        pass

    return render_template("signup.html")