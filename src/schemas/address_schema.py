from main import ma
from marshmallow import fields

#Address Schema
class AddressSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("address_id", "street_number", "street_name", "suburb", "city", "state", "post_code")

# Single address schema
address_schema = AddressSchema()
# Multiple addresss schema
addresses_schema =  AddressSchema (many=True)