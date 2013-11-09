from yearplan import db
from entity import Entity
from user import User
from sheet import Sheet

class UserSheet( Entity ):
   sheet = db.ReferenceField(Sheet)
   user = db.ReferenceField( User )
   starred = db.BooleanField(default=False)