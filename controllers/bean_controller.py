from flask import Blueprint, jsonify, request
from main import db
from models.beans import Bean
from models.orders import Order
from models.users import User
from schemas.bean_schema import bean_schema, beans_schema
from schemas.order_schema import order_schema, orders_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date

beans = Blueprint("bean", __name__, url_prefix="/beans")


@beans.route("/", methods=["GET"])
def get_bean():
    # get all the books from the database
    bean_list = Bean.query.all()
    result = beans_schema.dump(bean_list)
    return jsonify(result)

@beans.route("/<int:id>", methods=["GET"])
def get_bean(id):
    # get the bean from the database by id
    bean = Bean.query.get(id)
    result = bean_schema.dump(bean)
    return jsonify(result)

@beans.route("/", methods=["POST"])
# a token is needed for this request
@jwt_required()
def new_bean():
    # it is not enough with a token, the identity needs to be a librarian
    if get_jwt_identity() != "roaster":
        return {"error": "You don't have the permission to do this"}
    bean_fields = bean_schema.load(request.json)
    bean = Bean(
        country = bean_fields["country"],
        variety = bean_fields["variety"],
        flavour_notes = bean_fields["flavour_notes"],
        roast = bean_fields["roast"],
        recommended_preparation = bean_fields["recommended_preparation"],
        processing_method = bean_fields["processing_method"],
        roaster_id = bean_fields["roaster"]
    )

    db.session.add(bean)
    db.session.commit()
    return jsonify(bean_schema.dump(bean))

@beans.route("/<int:id>", methods=["PUT"])
@jwt_required()
def bean(id):
    # it is not enough with a token, the identity needs to be a librarian
    if get_jwt_identity() != "roaster":
        return {"error": "You don't have the permission to do this"}
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
    bean.roaster_id = bean_fields["roaster"]

    #save changes in the database
    db.session.commit() 

    return jsonify(bean_schema.dump(bean))   

# # get all bean varieties
# @beans.route("/order", methods=["GET"])
# @jwt_required()
# def get_all_orders():
#     # it is not enough with a token, the identity needs to be a roaster
#     if get_jwt_identity() != "roaster":
#         return {"error": "You don't have the permission to do this"}
#     # get all the orders from the database
#     reservations_list = Order.query.all()
#     result = orders_schema.dump(order_list)
#     return jsonify(result)
        
# # post a new reservation
# @books.route("<int:book_id>/reservations", methods=["POST"])
# @jwt_required()
# def new_reservation(book_id):
#     #find the book in the database
#     book = Book.query.get(book_id)
#     #check if book exist in the database
#     if not book:
#         return {"error": "Book id not found in the database"} 
#     user_id = get_jwt_identity()
#     user = User.query.get(user_id)
#     if not user:
#         return {"error": "User not found in the database"} 

#     reservation = Reservation(
#         user = user,
#         book = book,
#         start_date = date.today()
#     )

#     db.session.add(reservation)
#     db.session.commit()

#     return jsonify(reservation_schema.dump(reservation))
