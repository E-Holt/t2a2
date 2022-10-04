from datetime import timedelta
from flask import Blueprint, jsonify, request
from main import db
from main import bcrypt
from main import jwt
from flask_jwt_extended import create_access_token
from models.users import User
from schemas.user_schema import user_schema
from marshmallow.exceptions import ValidationError


user = Blueprint("user", __name__, url_prefix="/user")

#Register new user
@user.route("/register", methods=["POST"])
def register_user():
    #get the user details from the request
    user_fields = user_schema.load(request.json)
    #find user by username to check if they are already in the database
    user = User.query.filter_by(username=user_fields["username"]).first()
    if user:
        return {"error": "Username already exists in the database"}, 409

    #find user by email to check if they are already in the database
    user = User.query.filter_by(email=user_fields["email"]).first()
    if user:
        return {"error": "Email already exists in the database"}, 409
    #create user Object
    user = User(
        username = user_fields["username"],
        name = user_fields["name"],
        password =  bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8"),
        email = user_fields["email"],
        address_id = user_fields["address_id"]
    )

    #add the user to the database
    db.session.add(user)
    #save the changes in the database
    db.session.commit()

    #generate the token setting the identity (user.id) and expiry time (1 day)
    token = create_access_token(identity=str(user.user_id), expires_delta=timedelta(days=1)) 

    return {"username": user.username, "token": token}, 200

#Login user POST
@user.route("/login",methods = ["POST"])
def login_user():
    # Get username and password fron the request
    user_fields = user_schema.load(request.json)
    # Check username and password. User needs to exist, and password needs to match
    user = User.query.filter_by(username=user_fields["username"]).first()
    if not user:
        return {"error": "username is not valid"}, 404

    if not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return {"error": "wrong password"}, 409
    # Credentials are valid, so generate token and return it to the user

    token = create_access_token(identity=str(user.user_id), expires_delta=timedelta(days=1)) 

    return {"username": user.username, "token": token}, 200

@user.errorhandler(ValidationError)
def register_validation_error(error):
    return error.messages, 400