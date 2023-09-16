from flask import Blueprint, render_template

views = Blueprint("views", __name__)
#Blueprint means it contains a bunch of routes inside it

@views.route('/')
def home():
    return render_template("home.html")