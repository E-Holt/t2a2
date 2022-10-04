from main import ma
from marshmallow import fields
from schemas.roaster_schema import RoasterSchema

# Bean Schema
class BeanSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("bean_id", "country", "variety", "flavour_notes", "roast", "recommended_preparation", "processing_method", "roaster_id")

# Single bean schema
bean_schema = BeanSchema()
# Multiple bean schema
beans_schema = BeanSchema(many=True)
