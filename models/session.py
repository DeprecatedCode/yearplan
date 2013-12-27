from yearplan import db
from .base import BaseModel

class Session(BaseModel, db.Document):
    auth_id = db.StringField()
    