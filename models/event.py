from yearplan import db
from entity import Entity

class Event(Entity):
   dates = db.ListField( db.DateTimeField() )