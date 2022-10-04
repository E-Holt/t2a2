from main import ma
from marshmallow import fields
from schemas.bean_schema import BeanSchema
from schemas.user_schema import UserSchema

# Order Schema
class OrderSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("order_id", "order_date", "amount", "grind", "price", "user_id", "bean_id")

# Single order schema
order_schema = OrderSchema()
# Multiple order schema, not currently used other than for viewing
orders_schema = OrderSchema(many=True)