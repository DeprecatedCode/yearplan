from yearplan import db
from flask import url_for
from .entity import Entity

class User( Entity ):
   email = db.StringField()
   
   def to_json(self):
      return dict(name=self.name,
                  email=self.email,
                  description=self.description,
                  location=self.location,
                  public=self.public,
                  phone=self.phone,
                  links=self.links,
                  uri=url_for('UserView:get',id= self.id.__str__()),
                 )