from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Content, Screen,Composition
from . import db
from website import create_app
import json
import random, string

from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

views = Blueprint("views", __name__)
#Blueprint means it contains a bunch of routes inside it

# Temporary cache to store generated codes until they are verified
code_cache = {}


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
            new_content = Content(name=file.filename, user_id=current_user.id, file_type=type, file_path=dir_name)
            db.session.add(new_content)
            db.session.commit()
            #flash("Successfully Uploaded.", category="success")
            message='Successfully Uploaded.'
    return render_template("media.html", user=current_user, form=form, msg=message)

@views.route("/delete-content", methods=["POST"])
@login_required
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

            
#===================Screens/========================#


@views.route('/screens', methods=["GET", "POST"])
@login_required
def screens():
    return render_template('screens.html', user = current_user)


@views.route('/verify_code', methods=['POST'])
@login_required
def verify_code():
    """
    Verify a generated code.
    """
    print("++++++++++++++++Called++++++++++++++")
    code = request.json.get('code')
    print(code)
    print(code_cache)
    for entry in code_cache:
        if code == entry:
            del code_cache[code]
            print("+++++++++++")
            return jsonify({'status': 'success'})
            
    print("---------------")
    return jsonify({'status': 'fail'})


@views.route('/generate_code', methods=['GET'])
def generate_code():
    """
    Generate a 6-character code combining uppercase letters and digits.
    """
    print("=========================")
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    code_cache[code] = True
    return jsonify({'code': code})

@views.route("/add-screen", methods=["POST"])
@login_required
def addScreen():
    print("Executing")
    data = json.loads(request.data)

    existing_screen = Screen.query.filter_by(code=data['code']).first()
    message=""
    
    if existing_screen:
        message = "Screen already exists"
        return render_template("screens.html", user=current_user, msg=message)


    screen = Screen(user_id=current_user.id, code=data['code'], name=data['name'], location=data['location'], status=data['status'])
    db.session.add(screen)
    db.session.commit()

    return render_template("screens.html", user=current_user, msg=message)


@views.route("/delete-screen", methods=["POST"])
@login_required
def deleteScreen():
    data = json.loads(request.data)
    screenID = data["screenID"]
    screen = Screen.query.get(screenID)
    
    if screen:
        if screen.user_id == current_user.id:
            db.session.delete(screen)
            db.session.commit()
            print("Deleted")
            
    return render_template("screens.html", user=current_user)

@views.route("/render", methods=["GET","POST"])
@login_required
def render():
    return render_template("render.html", user=current_user)



@views.route("/getContent", methods=["GET"])
@login_required
def getMedia():
    print(current_user.contents[0].id)
    # return current_user

    try:
        # Query the 'name' and 'file_type' attributes from the 'Content' table
        content_query = db.session.query(Content.name, Content.file_type,Content.id).all()

        # Convert the query results to a list of dictionaries
        content_list = [{"name": name, "file_type": file_type, 'id':id} for name, file_type ,id in content_query]
        print(jsonify(content_list))
        return jsonify(content_list)

    except Exception as e:
        return {"No Media, please upload"}







@views.route("/addComposition", methods=["GET"])
@login_required
def addComposition():
    print(current_user.contents)
    return render_template("composition.html", user=jsonify({"id":current_user.id}).json)



@views.route("/saveComposition", methods=["POST"])
@login_required
def saveComposition():
    print("Executing")
    data = json.loads(request.data)

    #existing_composition = Composition.query.filter_by(code=data['code']).first()
    contents = Content.query.filter(Content.id.in_(data["content_ids"])).all()
    
    # if existing_screen:
    #     message = "Screen already exists"
    #     return render_template("screens.html", user=current_user, msg=message)

    print(data)
    composition = Composition(user_id=current_user.id, name=data['name'], description=data['description'], duration="")
    composition.contents.extend(contents)

    db.session.add(composition)
    db.session.commit()
    message="Successfully Added"
    print("Executingsdfghghhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    return render_template("screens.html", user=current_user, msg=message)


