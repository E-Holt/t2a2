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

# Database commands for flask
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

# Added multiple items for each table to allow for testing 
@db_commands.cli.command('seed')
def seed_db():

    address1 = Address(
    street_number = "1",
    street_name = "Example street",
    suburb = "Suburb",
    city = "Brisbane",
    state = "QLD",
    post_code = "5555"
    )
    db.session.add(address1) 
    db.session.commit()


    address2 = Address(
    street_number = "2",
    street_name = "Example street",
    suburb = "Suburb",
    city = "Brisbane",
    state = "QLD",
    post_code = "5555"
    )
    db.session.add(address2) 
    db.session.commit()

    address3 = Address(
    street_number = "3",
    street_name = "Example street",
    suburb = "Suburb",
    city = "Brisbane",
    state = "QLD",
    post_code = "5555"
    )
    db.session.add(address3) 
    db.session.commit()

    address4 = Address(
    street_number = "4",
    street_name = "Example street",
    suburb = "Suburb",
    city = "Brisbane",
    state = "QLD",
    post_code = "5555"
    )
    db.session.add(address4) 
    db.session.commit()

    roaster1 = Roaster(
    username = "ExampleRoaster1",
    name = "Example Roastery 1",
    password = bcrypt.generate_password_hash("12345678").decode("utf-8"),
    email = "roaster1@email.com",
    address_id = address1.address_id
    )
    db.session.add(roaster1) 
    db.session.commit()

    roaster2 = Roaster(
    username = "ExampleRoaster2",
    name = "Example Roastery 2",
    password = bcrypt.generate_password_hash("12345678").decode("utf-8"),
    email = "roaster2@email.com",
    address_id = address2.address_id
    )
    db.session.add(roaster2) 
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

    bean2 = Bean(
    country = "Indonesia",
    variety = "Abyssinia",
    flavour_notes = "berries, melon, spice, earthiness",
    roast = "medium",
    recommended_preparation = "Pour over",
    processing_method = "natural",
    roaster_id = roaster2.roaster_id
    )

    db.session.add(bean2) 
    db.session.commit()

    bean3 = Bean(
    country = "Ethiopia",
    variety = "JARC",
    flavour_notes = "juicy, clean, pineapple, green grape",
    roast = "medium",
    recommended_preparation = "press",
    processing_method = "anaerobic natural",
    roaster_id = roaster1.roaster_id
    )

    db.session.add(bean3) 
    db.session.commit()

    bean4 = Bean(
    country = "Kenya",
    variety = "SL28",
    flavour_notes = "sweet, syrupy, cherry, peach, orange",
    roast = "medium",
    recommended_preparation = "espresso",
    processing_method = "washed",
    roaster_id = roaster2.roaster_id
    )

    db.session.add(bean4) 
    db.session.commit()

    user1 = User(
    username = "user1",
    name = "Name Name",
    password = bcrypt.generate_password_hash("12345678").decode("utf-8"),
    email = "user1@email.com",
    address_id = address3.address_id
    )

    db.session.add(user1) 
    db.session.commit()

    user2 = User(
    username = "user2",
    name = "Name2 Name",
    password = bcrypt.generate_password_hash("12345678").decode("utf-8"),
    email = "user2@email.com",
    address_id = address4.address_id
    )

    db.session.add(user2) 
    db.session.commit()

    order1 = Order(
    order_date = date(day = 22, month = 9, year = 2020),
    amount = "250",
    grind = "coarse",
    price = "17",
    user_id = user1.user_id, 
    bean_id = bean1.bean_id
    )
    db.session.add(order1) 
    db.session.commit()

    order2 = Order(
    order_date = date(day = 26, month = 9, year = 2020),
    amount = "250",
    grind = "fine",
    price = "17",
    user_id = user2.user_id, 
    bean_id = bean2.bean_id
    )
    db.session.add(order2) 
    db.session.commit()

    print('Tables seeded')