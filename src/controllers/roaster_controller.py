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

# Register a new roaster
@roaster.route("/register", methods=["POST"])
def register_roaster():
    # Get the roaster details from the request
    roaster_fields = roaster_schema.load(request.json)
    # Check if username already exists in the database
    roaster = Roaster.query.filter_by(username=roaster_fields["username"]).first()
    # Error if username already exists
    if roaster:
        return {"error": "Username already exists in the database"}, 409

    # Check if email already exists in the database
    roaster = Roaster.query.filter_by(email=roaster_fields["email"]).first()
    # Error if email already exists in the database
    if roaster:
        return {"error": "Email already exists in the database"}, 409

    # Create roaster Object
    roaster = Roaster(
        username = roaster_fields["username"],
        email = roaster_fields["email"],
        password =  bcrypt.generate_password_hash(roaster_fields["password"]).decode("utf-8")
    )

    # Add the roaster to the database
    db.session.add(roaster)
    # Save the changes in the database
    db.session.commit()

    # Generate the token setting the identity (roaster.id) and expiry time (1 day)
    token = create_access_token(identity=str(roaster.roaster_id), expires_delta=timedelta(days=1)) 

    return {"username": roaster.username, "token": token}, 200

# Login a roaster that is already in the system
@roaster.route("/login",methods = ["POST"])
def login_roaster():
    # Get username and password from the request
    roaster_fields = roaster_schema.load(request.json)
    # Check username and password. Roaster needs to exist, and password must match
    roaster = Roaster.query.filter_by(username=roaster_fields["username"]).first()
    # Error if usename not valid
    if not roaster:
        return {"error": "That username is not valid"}, 404
    # Error if password doesn't match
    if not bcrypt.check_password_hash(roaster.password, roaster_fields["password"]):
        return {"error": "wrong password"}

    # Credentials are valid, so generate token and return it to the roster
    token = create_access_token(identity=str(roaster.roaster_id), expires_delta=timedelta(days=1)) 

    return {"username": roaster.username, "token": token}, 200

# Error handling if fields are filled in incorrectly
@roaster.errorhandler(ValidationError)
def register_validation_error(error):
    return error.messages, 400