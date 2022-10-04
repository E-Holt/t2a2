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

order = Blueprint("order", __name__, url_prefix="/order")

# Show all current orders
@order.route("/", methods=["GET"])
@jwt_required()
def get_order():
    # The orders can only be viewed by roasters with an appropriate authorization token
    roaster_id = get_jwt_identity()
    roaster = Roaster.query.get(roaster_id)
    # If the token isn't attached to a roaster, error
    if not roaster:
        return {"error": "You don't have the permission to do this"}, 401

    # Get all the orders from the database
    order_list = Order.query.all()
    # Show all the current orders
    result = orders_schema.dump(order_list)
    return jsonify(result), 200

# Post a new order using a specific bean id
@order.route("/<int:id>", methods=["POST"])
@jwt_required()
def new_order(id):
    # Only users can create orders, must be a user with an authorization token
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    # Error if not a user
    if not user:
        return {"error": "You don't have the permission to do this"}, 401

    # Find the requested bean in the database
    bean = Bean.query.get(id)
    # If that bean doesn't exist, error
    if not bean:
        return {"error": "That bean variety isn't currently available"}, 404
    # Fields that must be filled in to create a new order
    order_fields = order_schema.load(request.json)
    order = Order(
        order_date = order_fields["order_date"],
        amount = order_fields["amount"],
        grind = order_fields["grind"],
        price = order_fields["price"],
        user_id = order_fields["user_id"],
        bean_id = order_fields["bean_id"]
    )

    # Adds and commits the new order to the database
    db.session.add(order)
    db.session.commit()

    return jsonify(order_schema.dump(order)), 200

# Allows roaster to delete orders that have been fufilled
@order.route("/delete/<int:order_id>", methods=["DELETE"])
@jwt_required()
def delete_order(order_id):
    # Only roasters can view and delete orders, must have authorization token
    roaster_id = get_jwt_identity()
    roaster = Roaster.query.get(roaster_id)
    # If not a roaster, error
    if not roaster:
        return {"error": "You don't have the permission to do this"}, 401

    # Find the specific order in the database
    order = Order.query.get(order_id)
    # If the order doesn't exist, error
    if not order:
        return {"error": "That order is not found in the database"}, 404

    # Delete the order from the database
    db.session.delete(order) 
    db.session.commit() 

    return jsonify(order_schema.dump(order)), 200   

# Error handler if fields aren't correctly filled out
@order.errorhandler(ValidationError)
def register_validation_error(error):
    return error.messages, 400