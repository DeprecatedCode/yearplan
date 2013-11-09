from yearplan import db
from flask import url_for
from .entity import Entity

class User( Entity ):
   email = db.StringField()
   
   def __dict__(self):
      return {
            #'id' : self.id.__str__(),
            'name' : self.name,
            'email': self.email,
            'uri' : url_for('UserView:get',id= self.id.__str__())
         }