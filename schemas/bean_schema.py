from main import ma
from marshmallow import fields
from schemas.roaster_schema import RoasterSchema

class BeanSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("bean_id", "country", "variety", "flavour_notes", "roast", "recommended_preparation", "processing_method", "roaster")
        load_only = ("roaster_id")
    # Schema is defined as a String, to avoid te circular import error 
    roaster = fields.Nested("RoasterSchema", only=("name"))

#single bean schema
bean_schema = BeanSchema()
#multiple bean schema
beans_schema = BeanSchema(many=True)
