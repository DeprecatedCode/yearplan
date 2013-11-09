from yearplan import db
from .base import BaseModel

class Session(BaseModel):
   auth_id = db.StringField()