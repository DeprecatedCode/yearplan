from yearplan import db
from entity import Entity
from flask import url_for
from models import Sheet

class Event(Entity):
   dates = db.ListField( db.DateTimeField() )
   sheet = db.ReferenceField(Sheet)
   
   def to_json(self): 
      return { 'name' : self.name,
               'description' : self.description,
               'location': self.location,
               'phone' : self.phone,
               'public':self.public,
               'links' : self.links,
               'color' : self.color,
               'alive' : self.alive,
               'dates' : self.dates,
               'uri' : url_for('EventView:get',id= str(self.id))
      }