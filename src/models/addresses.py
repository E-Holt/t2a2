from main import db

class Address(db.Model):
    # Define the tablename in the database as addresses
    __tablename__ = "addresses"
    # setting the columns 
    address_id = db.Column(db.Integer, primary_key=True)
    street_number = db.Column(db.Integer)
    street_name = db.Column(db.String())
    suburb = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String())
    post_code = db.Column(db.Integer)
