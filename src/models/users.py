from main import db

class User(db.Model):
    # Define the tablename in the database as users
    __tablename__= "users"
    # Setting the columns 
    user_id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(), nullable=False, unique=True)
    name = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.address_id"), nullable=False)
    # Address id is a forign key