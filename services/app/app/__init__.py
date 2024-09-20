from flask import Flask, request, redirect, url_for, render_template, flash, session, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
import os
from .models import db, User, Note
import requests

#Flask Config Object
class Config(object):
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "postgresql://")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SECRET_KEY: str =  os.getenv("FLASK_SECRET")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET")


#Initializing application
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
jwt = JWTManager(app)

#Constants (Actually should be in a separate file but...)
yandex_speller_url = 'https://speller.yandex.net/services/spellservice.json/checkText'


#JWT Stuff
@jwt.user_identity_loader
def user_identity_lookup(user: User) -> int:
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header: dict, jwt_data: dict) -> User | None:
    identity: int = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


#Authentication route.
@app.route("/api/authenticate", methods=["POST"])
def authenticate() -> dict:
    data: dict = request.json
    username: str|None = data.get("username", None)
    password: str|None = data.get("password", None)
    user: User | None = User.query.filter_by(username=username).one_or_none()

    if not user or not user.check_password(password):
        return jsonify({"error":{
            "code":401,
            "message":"Bad username or password!"
            }
        }), 401

    # Notice that we are passing in the actual sqlalchemy user object here
    access_token: str = create_access_token(identity=user)
    return jsonify(access_token=access_token)

#Notes routes section
#Get all notes
@app.route("/api/notes", methods=["GET"])
@jwt_required()
def get_all_notes() -> dict: 
    current_user: int = get_jwt_identity()

    if not current_user:
        return jsonify({"error":{
            "code":401,
            "message":"No proper authentication token was found in request!"
            }
        }), 401

    current_user: User = User.get_by_id(current_user)
    notes: list = current_user.notes
    print(type(notes))

    return jsonify({'data':[note.to_dict() for note in notes]}),200


#Notes routes section
#Get a single note
@app.route("/api/notes/<int:note_id>", methods=["GET"])
@jwt_required()
def get_note(note_id) -> dict:
    current_user: int = get_jwt_identity()
    if not current_user:
        return jsonify({"error":{
            "code":401,
            "message":"No proper authentication token was found in request!"
            }
        }), 401

    current_user: User = User.get_by_id(current_user)
    note: Note | None = current_user.notes.filter_by(id=note_id).first() #This line ensures that user has access only to their own notes!

    if not note:
        return jsonify({'error':
            {'code':404,
            'message': 'No such note found.'
            }}), 404

    return jsonify({'data':note.to_dict()}),200

#Add a note
#User must provide name of the note and its content
#If provided content pass grammar check - it gets inserted into the according table
#Else - server just returns found grammar mistakes
@app.route("/api/notes/new", methods=["POST"])
@jwt_required()
def add_note() -> dict:
    current_user: int = get_jwt_identity()
    if not current_user:
        return jsonify({"error":{
            "code":401,
            "message":"No proper authentication token was found in request!"
            }
        }), 401

    current_user: User = User.get_by_id(current_user)
    
    data: dict = request.json
    name: str|None = data.get("name", None)
    content: str|None = data.get("content", None)

    speller_response: requests.Response = requests.post(yandex_speller_url, data={'text':content})
    if speller_response.json():
        return jsonify({"error": {
            "code":400,
            "message":'Yandex speller has found mistakes in the given note content. Its creation request has been declined.',
            'speller_response': speller_response.json()
            }}),400

    note: Note = Note(name=name,content=content,owner_id=current_user.id)
    db.session.add(note)
    db.session.commit()

    return {},201


#Testing route
@app.route("/api/hello", methods=["GET"])
def hello() -> str:
    return "HELLO"

if __name__ == "__main__":
    db.init_app(app)
    app.run(host='0.0.0.0')