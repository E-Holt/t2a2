from main import db

class Roaster(db.Model):
    #define the tablename in the database as roasters
    __tablename__="roasters"
    # setting the columns 
    roaster_id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(), nullable=False, unique=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.address_id"), nullable=False)