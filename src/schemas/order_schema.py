from main import ma
from marshmallow import fields
from schemas.bean_schema import BeanSchema
from schemas.user_schema import UserSchema

class OrderSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("order_id", "order_date", "amount", "grind", "price", "user_id", "bean_id")

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)