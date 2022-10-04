from main import db

class Order(db.Model):
    # Define the tablename in the database as orders
    __tablename__ = "orders"
    # Setting the columns 
    order_id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.Date(), nullable=False)
    amount = db.Column(db.Integer, default = 250)
    grind = db.Column(db.String())
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    bean_id = db.Column(db.Integer, db.ForeignKey("beans.bean_id"), nullable=False)
    # User id and bean id are forign keys
