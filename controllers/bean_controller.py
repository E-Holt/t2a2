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

bean = Blueprint("bean", __name__, url_prefix="/bean")

@bean.route("/", methods=["GET"])
def get_bean():
    # get all the bean from the database
    bean_list = Bean.query.all()
    result = beans_schema.dump(bean_list)
    return jsonify(result)

@bean.route("/<int:id>", methods=["GET"])
def get_bean_id(id):
    # get the bean from the database by id
    bean = Bean.query.get(id)
    result = bean_schema.dump(bean)
    return jsonify(result)

@bean.route("/add", methods=["POST"])
# a token is needed for this request
@jwt_required()
def add_bean():
    roaster_id = get_jwt_identity()
    roaster = Roaster.query.get(roaster_id)
    # it is not enough with a token, the identity needs to be a librarian
    if not roaster:
        return {"error": "You don't have the permission to do this"}, 401
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

    db.session.add(bean)
    db.session.commit()
    return jsonify(bean_schema.dump(bean))

@bean.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_bean(id):
    roaster_id = get_jwt_identity()
    roaster = Roaster.query.get(roaster_id)
    # it is not enough with a token, the identity needs to be a librarian
    if not roaster:
        return {"error": "You don't have the permission to do this"}, 401
    #find the bean in the database
    bean = Bean.query.get(id)
    #check if bean exist in the database
    if not bean:
        return {"error": "That bean variety is not found in the database"}
    #get the bean details from the request
    bean_fields = bean_schema.load(request.json)
    #update the values of the bean
    bean.country = bean_fields["country"]
    bean.variety = bean_fields["variety"]
    bean.flavour_notes = bean_fields["flavour_notes"]
    bean.roast = bean_fields["roast"]
    bean.recommended_preparation = bean_fields["recommended_preparation"]
    bean.processing_method = bean_fields["processing_method"]
    bean.roaster_id = bean_fields["roaster_id"]

    #save changes in the database
    db.session.commit() 

    return jsonify(bean_schema.dump(bean))   

# # show all bean varieties
# @bean.route("/", methods=["GET"])
# @jwt_required()
# def get_all_orders():
#     # it is not enough with a token, the identity needs to be a roaster
#     if get_jwt_identity() != "roaster":
#         return {"error": "You don't have the permission to do this"}
#     # get all the orders from the database
#     reservations_list = Order.query.all()
#     result = orders_schema.dump(order_list)
#     return jsonify(result)
        
# post a new order
@bean.route("/order/<int:id>", methods=["POST"])
@jwt_required()
def new_order(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    # it is not enough with a token, the identity needs to be a user
    if not user:
        return {"error": "You don't have the permission to do this"}, 401
    #find the book in the database
    bean = Bean.query.get(id)
    #check if book exist in the database
    if not bean:
        return {"error": "That bean variety isn't currently available"} 
    order_fields = order_schema.load(request.json)
    order = Order(
        order_date = order_fields["order_date"],
        amount = order_fields["amount"],
        grind = order_fields["grind"],
        price = order_fields["price"],
        user_id = order_fields["user_id"],
        bean_id = order_fields["bean_id"]
    )

    db.session.add(order)
    db.session.commit()

    return jsonify(order_schema.dump(order))
