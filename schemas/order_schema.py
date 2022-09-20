from main import ma
from marshmallow import fields
from schemas.bean_schema import BeanSchema
from schemas.user_schema import UserSchema

class OrderSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('order_id', "order_date", "amount", "grind", "price", "user", "bean")
        load_only = ("user_id", "bean_id")
    user = fields.Nested(UserSchema, only=("user_name"))
    bean = fields.Nested(BeanSchema, only=("variety"))
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)