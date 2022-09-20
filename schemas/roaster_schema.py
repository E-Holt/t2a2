from wsgiref import validate
from main import ma
from marshmallow.validate import Length

class RoasterSchema(ma.Schema):
    class Meta:
        fields = ("roaster_id", "username", "name", "email", "password", "address_id")
    #add validation to password
    password = ma.String(validate=Length(min=8))

roaster_schema = RoasterSchema()
#multiple schema not necessary right now
