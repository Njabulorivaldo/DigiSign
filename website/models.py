from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class Content(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    file_type = db.Column(db.String(150))
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())
    file_path = db.Column(db.String(10000))


class Image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content_id = db.Column(db.Integer, db.ForeignKey("content.id"))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class Screens(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content_id = db.Column(db.Integer, db.ForeignKey("content.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    location = db.Column(db.String(150))
    status = db.Column(db.String(150)) # Offline/ Online/ Maintenance
    contents = db.relationship("Content")

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    department = db.Column(db.String(150))
    contents = db.relationship("Content")
    screens = db.relationship("Screens")
