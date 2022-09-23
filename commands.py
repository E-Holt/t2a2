from flask import Blueprint
from main import db
from main import bcrypt
from models.addresses import Address
from models.beans import Bean
from models.users import User
from models.roasters import Roaster
from models.orders import Order
from datetime import date


db_commands = Blueprint("db", __name__)

@db_commands.cli.command('create')
def create_db():
    # Tell SQLAlchemy to create all tables for all models in the physical DB
    db.create_all()
    print('Tables created')

@db_commands.cli.command('drop')
def drop_db():
    # Tell SQLAlchemy to drop all tables
    db.drop_all()
    print('Tables dropped')

@db_commands.cli.command('seed')
def seed_db():

    address1 = Address(
    street_number = "123",
    street_name = "Example street",
    suburb = "Suburb",
    city = "Brisbane",
    state = "QLD",
    post_code = "5555"
    )
    db.session.add(address1) 
    db.session.commit()


    address2 = Address(
    street_number = "123",
    street_name = "Example2 street",
    suburb = "Suburb",
    city = "Brisbane",
    state = "QLD",
    post_code = "5555"
    )
    db.session.add(address2) 
    db.session.commit()

    roaster1 = Roaster(
    username = "ToastyRoaster",
    name = "Toasty Roastery",
    password = bcrypt.generate_password_hash("12345678").decode("utf-8"),
    email = "toasty@email.com",
    address_id = address1.address_id
    )
    db.session.add(roaster1) 
    db.session.commit()

    bean1 = Bean(
    country = "Panama",
    variety = "Geisha",
    flavour_notes = "Floral, citrus, rasin",
    roast = "light",
    recommended_preparation = "Pour over",
    processing_method = "Black Winey natural",
    roaster_id = roaster1.roaster_id
    )

    db.session.add(bean1) 
    db.session.commit()


    user1 = User(
    username = "user1",
    name = "Name Name",
    password = bcrypt.generate_password_hash("12345678").decode("utf-8"),
    email = "user1@email.com",
    address_id = address2.address_id
    )

    db.session.add(user1) 
    db.session.commit()

    order1 = Order(
    order_date = date(day = 22, month = 9, year = 2020),
    amount = "250",
    grind = "course",
    price = "17",
    user_id = user1.user_id, 
    bean_id = bean1.bean_id
    )
    db.session.add(order1) 
    db.session.commit()

    print('Tables seeded')