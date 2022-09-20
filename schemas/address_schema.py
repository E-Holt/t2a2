from main import ma
from marshmallow import fields

class AddressSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("address_id", "strees_number", "street_name", "suburb", "city", "state", "post_code")

address_schema = AddressSchema()
addresses_schema =  AddressSchema (many=True)