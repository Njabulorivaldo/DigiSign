from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Content
from . import db
from website import create_app
import json

from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

views = Blueprint("views", __name__)
#Blueprint means it contains a bunch of routes inside it



class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


def get_type(path):
    
    type = path[-4::].lower()
    images_types = ['.jpg', 'jpeg', '.png', '.gif', '.bmp', 'tiff', 'webp']
    video_types = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.m4v', '.ogg', '.ogv', '.mpg']

    
    if type == ".mp3":
        return "Audio"
    
    elif type in video_types:
        return "Video"
    
    elif type in images_types:
        return "Image"
    
    else:
        return None
    
def makeUserPath(dir):
    try: 
        os.mkdir(dir) 
    except OSError as error: 
        #User path already exists
        pass 


@views.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    return render_template('profile.html', user = current_user)

@views.route('/', methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template('dashboard.html', user = current_user)


@views.route('/screens', methods=["GET", "POST"])
@login_required
def screens():
    return render_template('screens.html', user = current_user)


@views.route("/media", methods=["GET", "POST"])
@login_required   
def media():
    app = create_app()
    form = UploadFileForm()
    message=""
    if form.validate_on_submit():
        file = form.file.data # First grab the file

        #Get the necessary paths for user and file
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'] +"/"+ str(current_user.id),secure_filename(file.filename))
        user_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'], str(current_user.id))
        dir_name = os.path.join(app.config['UPLOAD_FOLDER'], str(current_user.id), secure_filename(file.filename))
        
        #Checks if the user has a folder alreay existing, if not make a dir to store their files
        makeUserPath(user_dir)
        
        #Check if file is one of the accepted types/extensitons
        type = get_type(dir_name)


        if type == None:
            flash("You Can Only Upload Audio.mp3/Video.mp4/Image", category="error")
            message= "Unsupported Format"
        
        else:
            file.save(file_path) # Then save the file
            new_content = Content(user_id=current_user.id, file_type=type, file_path=dir_name)
            db.session.add(new_content)
            db.session.commit()
            #flash("Successfully Uploaded.", category="success")
            message='Successfully Uploaded.'
    return render_template("media.html", user=current_user, form=form, msg=message)

@views.route("/delete-content", methods=["POST"])
def deleteContent():
    content = json.loads(request.data)
    contentID = content["contentID"]
    content = Content.query.get(contentID)
    print(content.file_path)
    
    if content:
        if content.user_id == current_user.id:
            db.session.delete(content)
            db.session.commit()
            os.remove("../DigitalSign/website/"+content.file_path)
            
    return render_template("media.html", user=current_user)
