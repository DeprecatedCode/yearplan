from yearplan import db
from .base import BaseModel

class Entity(BaseModel):
    name = db.StringField(required=True)
    description = db.StringField(max_length=300)
    location = db.StringField(max_length=255 )
    links = db.ListField( db.StringField())
    color = db.StringField()
    tags = db.ListField()
    
    public = db.BooleanField()
    created_by = db.StringField()

