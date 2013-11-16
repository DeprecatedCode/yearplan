from yearplan import db
from entity import Entity
from user import User
from flask import url_for

class Sheet(Entity):
   created_by = db.ReferenceField(User)
   
   def to_json(self): 
      return dict(name=self.name,
                  description=self.description,
                  location=self.location,
                  phone=self.phone,
                  public=self.public,
                  created_by=url_for('UserView:get',id=str(self.created_by)),
                  links=self.links,
                  color=self.color,
                  alive=self.alive,
                  uri=url_for('SheetView:get',id= str(self.id))
                 )