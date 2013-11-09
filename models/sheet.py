from yearplan import db
from entity import Entity
from user import User

class Sheet(Entity):
   created_by = db.ReferenceField(User)