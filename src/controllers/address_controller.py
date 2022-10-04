from flask import Blueprint, jsonify, request
from main import db
from models.addresses import Address
from models.users import User
from models.roasters import Roaster
from schemas.address_schema import address_schema, addresses_schema
from schemas.user_schema import user_schema 
from schemas.roaster_schema import roaster_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError

address = Blueprint("address", __name__, url_prefix="/address")

# Show all current addresses
@address.route("/", methods=["GET"])
@jwt_required()
def get_address():
    # Must be a roaster to view addresses, must have roaster authorization token
    roaster_id = get_jwt_identity()
    roaster = Roaster.query.get(roaster_id)
    # If not a roaster, error
    if not roaster:
        return {"error": "You don't have the permission to do this"}, 401

    # Get all the addresses from the database
    address_list = Address.query.all()
    result = addresses_schema.dump(address_list)
    return jsonify(result), 200

# Post a new address by users or roasters
@address.route("/add", methods=["POST"])
@jwt_required()
def add_address():
    # All address fields must be filled in
    address_fields = address_schema.load(request.json)
    address = Address(
        street_number = address_fields["street_number"],
        street_name = address_fields["street_name"],
        suburb = address_fields["suburb"],
        city = address_fields["city"],
        state = address_fields["state"],
        post_code = address_fields["post_code"]
    )
    # Add and commit new address to database
    db.session.add(address)
    db.session.commit()

    return jsonify(address_schema.dump(address)), 200

# Error handler if fields aren't correctly filled out
@address.errorhandler(ValidationError)
def register_validation_error(error):
    return error.messages, 400

