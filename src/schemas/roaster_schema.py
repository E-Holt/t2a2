from wsgiref import validate
from main import ma
from marshmallow import fields
from marshmallow.validate import Length

# Roaster Schema
class RoasterSchema(ma.Schema):
    class Meta:
        fields = ("roaster_id", "username", "name", "email", "password", "address_id")
    # Add validation to password
    password = ma.String(validate=Length(min=8))

roaster_schema = RoasterSchema()
#multiple schema not necessary right now, but if needed:
#roasters_schema = RoasterSchema(many=True)
