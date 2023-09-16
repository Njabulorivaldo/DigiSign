from . import db 
from flask_login import UserMixin

class Content(db.Model):
    id = db.Column(db.Integer)
    type = db.Column(db.String)


class User(db.Model, UserMixin):

    user_id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    department = db.Column(db.String(150))