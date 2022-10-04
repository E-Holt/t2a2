from wsgiref import validate
from main import ma
from marshmallow.validate import Length

# User schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ("user_id", "username", "name", "email", "password", "address_id")
    # Add validation to password
    password = ma.String(validate=Length(min=8))

user_schema = UserSchema()
#multiple schema not necessary right now, but if needed:
#users_schema = UserSchema(many=True)