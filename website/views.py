from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Content

from website import create_app

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
    
    type = path[-4::] 
    print(type)
    audio_types = [".mp3",".wav",".flac",".ogg",".aac",".m4a",".wma",".aiff",".au",".ra",".mid",".midi",".amr",".ac3",".opus",".mka",".webm",".caf",".pcm",]
    images_types = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    video_types = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm']

    if type in audio_types:
        return "Audio"
    elif type in video_types:
        return "Video"
    elif type in images_types:
        return "Image"
    else:
        return None

@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    app = create_app()
    form = UploadFileForm()
    
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))

        #Check if file is one of the accepted types/extensitons
        type = get_type(file_path)
        print(type)

        if type == None:
            flash("You Can Only Upload Audio/Video/Image", category="error")
              
        else:
            file.save(file_path) # Then save the file
            flash("Successfully Uploaded.", category="success")


        #Getting the file type


        #new_content = Content(user_id=current_user.id, 

    return render_template('home.html', user = current_user, form=form)


'''def home():
    if request.method == "POST":
        content = request.form.get("content")

        if content:
            new_content = Content()
            flash("Content uploaded", category="success")
            pass

        else:
            flash("Upload valid content", category="error")

    return render_template("home.html", user=current_user)'''
