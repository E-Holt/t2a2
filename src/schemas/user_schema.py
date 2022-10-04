from wsgiref import validate
from main import ma
from marshmallow.validate import Length

class UserSchema(ma.Schema):
    class Meta:
        fields = ("user_id", "username", "name", "email", "password", "address_id")
    #add validation to password
    password = ma.String(validate=Length(min=8))

user_schema = UserSchema()
#multiple schema not necessary right now
#users_schema = UserSchema(many=True)