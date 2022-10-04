from flask import Blueprint, jsonify, request
from main import db
from models.beans import Bean
from models.orders import Order
from models.users import User
from models.roasters import Roaster
from schemas.bean_schema import bean_schema, beans_schema
from schemas.order_schema import order_schema, orders_schema
from schemas.roaster_schema import roaster_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date
from marshmallow.exceptions import ValidationError

bean = Blueprint("bean", __name__, url_prefix="/bean")

# Shows all the current bean varieties in the database
@bean.route("/", methods=["GET"])
def get_bean():
    # Gets and displays all the bean from the database
    bean_list = Bean.query.all()
    result = beans_schema.dump(bean_list)
    return jsonify(result), 200

# Search function for different bean criteria, I attempted to make this more efficient but was unable to do so
@bean.route("/search", methods=["GET"])
def search_beans():
    filtered_beans_list = []

    # Search for specific citeria
    if request.args.get("variety"):
        filtered_beans_list = Bean.query.filter_by(variety = request.args.get("variety"))
    elif request.args.get("country"):
        filtered_beans_list = Bean.query.filter_by(country = request.args.get("country"))
    elif request.args.get("flavour_notes"):
        filtered_beans_list = Bean.query.filter_by(flavour_notes = request.args.get("flavour_notes"))
    elif request.args.get("processing_method"):
        filtered_beans_list = Bean.query.filter_by(processing_method = request.args.get("processing_method"))
    elif request.args.get("recommended_preparation"):
        filtered_beans_list = Bean.query.filter_by(recommended_preparation = request.args.get("recommended_preparation"))
    elif request.args.get("roast"):
        filtered_beans_list = Bean.query.filter_by(roast = request.args.get("roast"))
    # Error if no bean varieties fit search criteria
    else:
        return {"error": "No beans available based on that search criteria"}, 404
    # Show all the beans from the database filtered by criteria
    result = beans_schema.dump(filtered_beans_list)
    return jsonify(result), 200

# Search function for specific bean variety id 
@bean.route("/<int:id>", methods=["GET"])
def get_bean_id(id):
    # Get the bean from the database by id
    bean = Bean.query.get(id)
    result = bean_schema.dump(bean)
    return jsonify(result), 200

# Add a new bean variety
@bean.route("/add", methods=["POST"])
@jwt_required()
def add_bean():
    # Only roasters can add a new bean, must have roaster authorization token
    roaster_id = get_jwt_identity()
    roaster = Roaster.query.get(roaster_id)
    # If not a roaster, error
    if not roaster:
        return {"error": "You don't have the permission to do this"}, 401
    # Fields must be filled in to add new bean variety
    bean_fields = bean_schema.load(request.json)
    bean = Bean(
        country = bean_fields["country"],
        variety = bean_fields["variety"],
        flavour_notes = bean_fields["flavour_notes"],
        roast = bean_fields["roast"],
        recommended_preparation = bean_fields["recommended_preparation"],
        processing_method = bean_fields["processing_method"],
        roaster_id = bean_fields["roaster_id"]
    )
    # Add and commit new bean variety to the database
    db.session.add(bean)
    db.session.commit()
    return jsonify(bean_schema.dump(bean))

# Update a bean variety
@bean.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_bean(id):
    # Only roasters can edit bean varieties. Must have roaster authorization token
    roaster_id = get_jwt_identity()
    roaster = Roaster.query.get(roaster_id)
    # If not a roaster, error
    if not roaster:
        return {"error": "You don't have the permission to do this"}, 401

    # Find the specific bean in the database
    bean = Bean.query.get(id)
    # If that bean variety doesn't exist, error
    if not bean:
        return {"error": "That bean variety is not found in the database"}, 404

    # Get the bean variety details from the request
    bean_fields = bean_schema.load(request.json)

    # Update the values of the bean fields
    bean.country = bean_fields["country"]
    bean.variety = bean_fields["variety"]
    bean.flavour_notes = bean_fields["flavour_notes"]
    bean.roast = bean_fields["roast"]
    bean.recommended_preparation = bean_fields["recommended_preparation"]
    bean.processing_method = bean_fields["processing_method"]
    bean.roaster_id = bean_fields["roaster_id"]

    # Save changes in the database
    db.session.commit() 

    return jsonify(bean_schema.dump(bean)), 200   

# Delete a bean variety that is no longer available
@bean.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_bean(id):
    # Only roasters can delete bean varieties, must have roaster authorization token
    roaster_id = get_jwt_identity()
    roaster = Roaster.query.get(roaster_id)
    # If not a roaster, error
    if not roaster:
        return {"error": "You don't have the permission to do this"}, 401

    # Find the specific bean in the database
    bean = Bean.query.get(id)
    # If the bean variety doesn't exist, error
    if not bean:
        return {"error": "That bean variety is not found in the database"}, 404
    # Get the bean details from the request
    bean_fields = bean_schema.load(request.json)

    # Delete the bean in the database
    db.session.delete(bean) 
    db.session.commit() 

    return jsonify(bean_schema.dump(bean)), 200   

# Error handler if fields aren't correctly filled out
@bean.errorhandler(ValidationError)
def register_validation_error(error):
    return error.messages, 400