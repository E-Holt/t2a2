from datetime import timedelta
from flask import Blueprint, jsonify, request
from models.roasters import Roaster
from main import db
from main import bcrypt
from main import jwt
from flask_jwt_extended import create_access_token
from schemas.roaster_schema import roaster_schema
from marshmallow.exceptions import ValidationError

roaster = Blueprint("roaster", __name__, url_prefix="/roaster")

#Register new roaster
@roaster.route("/register", methods=["POST"])
def register_roaster():
    #get the roaster details from the request
    roaster_fields = roaster_schema.load(request.json)
    #find roaster by username to check if they are already in the database
    roaster = Roaster.query.filter_by(username=roaster_fields["username"]).first()
    if roaster:
        return {"error": "Username already exists in the database"}, 409

    #find roaster by email to check if they are already in the database
    roaster = Roaster.query.filter_by(email=roaster_fields["email"]).first()
    if roaster:
        return {"error": "Email already exists in the database"}, 409
    #create roaster Object
    roaster = Roaster(
        username = roaster_fields["username"],
        email = roaster_fields["email"],
        password =  bcrypt.generate_password_hash(roaster_fields["password"]).decode("utf-8")
    )

    #add the roaster to the database
    db.session.add(roaster)
    #save the changes in the database
    db.session.commit()

    #generate the token setting the identity (roaster.id) and expiry time (1 day)
    token = create_access_token(identity=str(roaster.roaster_id), expires_delta=timedelta(days=1)) 

    return {"username": roaster.username, "token": token}, 200

#Login a roaster that is already in the system
@roaster.route("/login",methods = ["POST"])
def login_roaster():
    # Get username and password from the request
    roaster_fields = roaster_schema.load(request.json)
    # Check username and password. Roaster needs to exist, and password must match
    roaster = Roaster.query.filter_by(username=roaster_fields["username"]).first()
    if not roaster:
        return {"error": "That username is not valid"}, 404
    
    if not bcrypt.check_password_hash(roaster.password, roaster_fields["password"]):
        return {"error": "wrong password"}

    # Credentials are valid, so generate token and return it to the roster
    token = create_access_token(identity=str(roaster.roaster_id), expires_delta=timedelta(days=1)) 

    return {"username": roaster.username, "token": token}, 200

@roaster.errorhandler(ValidationError)
def register_validation_error(error):
    return error.messages, 400