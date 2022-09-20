from main import db

class User(db.Model):
    #define the tablename in the database as users
    __tablename__="users"
    # setting the columns 
    user_id = db.Column(db.Integer, primary_key =True)
    user_name = db.Column(db.String(), nullable=False, unique=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.address_id"), nullable=False)