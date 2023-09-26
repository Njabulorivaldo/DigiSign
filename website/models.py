from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func


# Association table for the many-to-many relationship between Screen and Content
screen_content = db.Table('screen_content',
    db.Column('screen_id', db.Integer, db.ForeignKey('screen.id'), primary_key=True),
    db.Column('content_id', db.Integer, db.ForeignKey('content.id'), primary_key=True)
)

# Association table for the many-to-many relationship between Composition and Content
composition_content = db.Table('composition_content',
    db.Column('composition_id', db.Integer, db.ForeignKey('composition.id'), primary_key=True),
    db.Column('content_id', db.Integer, db.ForeignKey('content.id'), primary_key=True)
)


class Content(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.String(150))
    file_type = db.Column(db.String(150))
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())
    file_path = db.Column(db.String(10000))


class Image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content_id = db.Column(db.Integer, db.ForeignKey("content.id"))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class Screen(db.Model):
    # id = db.Column(db.Integer, primary_key = True)
    # content_id = db.Column(db.Integer, db.ForeignKey("content.id"))
    # user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # location = db.Column(db.String(150))
    # status = db.Column(db.String(150)) # Offline/ Online/ Maintenance
    # contents = db.relationship("Content")

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    code = db.Column(db.String(6), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(150), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    composition_id = db.Column(db.Integer, db.ForeignKey('composition.id'), nullable=True)

    # Relationship
    contents = db.relationship('Content', secondary=screen_content, lazy='subquery', 
                               backref=db.backref('screens', lazy=True))
  


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    department = db.Column(db.String(150))

    contents = db.relationship("Content")
    screens = db.relationship("Screen")
    compositions = db.relationship('Composition', backref='user', lazy=True) 

class Composition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Each composition belongs to one user
    duration = db.Column(db.String(50), nullable=True)

        # Relationships
    screens = db.relationship('Screen', backref='composition', lazy=True)
    contents = db.relationship('Content', secondary=composition_content, lazy='subquery', 
                               backref=db.backref('compositions', lazy=True))  # Composition can have many contents

