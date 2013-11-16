from yearplan import db, app_salt
from .base import BaseModel
from .user import User
import hashlib

class Auth(BaseModel):
   user = db.ReferenceField(User)
   sessions = db.ListField( )
   password = db.StringField(max_length=255)
   # hash -> auth_id + session_id 
   hash = db.StringField()

   def hash_password(self, email, password ):
      _hashed = hashlib.md5( email.lower() + password + app_salt )
      return _hashed.hexdigest()