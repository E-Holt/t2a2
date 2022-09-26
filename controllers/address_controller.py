from flask import Blueprint, jsonify, request
from main import db
from models.addresses import Address
from models.users import User
from models.roasters import Roaster
from schemas.address_schema import address_schema, addresses_schema
from schemas.user_schema import user_schema 
from schemas.roaster_schema import roaster_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

address = Blueprint("address", __name__, url_prefix="/address")

# Show all current addresses
@address.route("/", methods=["GET"])
@jwt_required()
def get_address():
    roaster_id = get_jwt_identity()
    roaster = Roaster.query.get(roaster_id)
    # only roasters should be able to access all addresses
    if not roaster:
        return {"error": "You don't have the permission to do this"}, 401
    # get all the addresses from the database
    address_list = Address.query.all()
    result = addresses_schema.dump(address_list)
    return jsonify(result)

# Post a new address by users or roasters
@address.route("/add", methods=["POST"])
@jwt_required()
def add_address():
    address_fields = address_schema.load(request.json)
    address = Address(
        street_number = address_fields["street_number"],
        street_name = address_fields["street_name"],
        suburb = address_fields["suburb"],
        city = address_fields["city"],
        state = address_fields["state"],
        post_code = address_fields["post_code"]
    )

    db.session.add(address)
    db.session.commit()

    return jsonify(address_schema.dump(address))

