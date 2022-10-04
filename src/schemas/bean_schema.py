from main import ma
from marshmallow import fields
from schemas.roaster_schema import RoasterSchema

class BeanSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("bean_id", "country", "variety", "flavour_notes", "roast", "recommended_preparation", "processing_method", "roaster_id")
#single bean schema
bean_schema = BeanSchema()
#multiple bean schema
beans_schema = BeanSchema(many=True)
