from yearplan import db
from .base import BaseModel
from .user import User

class Auth(BaseModel):
   user = db.ReferenceField(User)
   sessions = db.ListField( )
   password = db.StringField(max_length=255)
   # hash -> auth_id + session_id 
   hash = db.StringField()