from yearplan import db
from entity import Entity
from user import User
from sheet import Sheet
from flask import url_for

class UserSheet( Entity ):
   sheet = db.ReferenceField(Sheet)
   user = db.ReferenceField( User )
   starred = db.BooleanField(default=False)
   
   def to_json(self): 
      return dict(name=self.name,
                  sheet=self.sheet.to_json(),
                  user = self.user.to_json(),
                  public=self.sheet.public,
                  starred=self.starred,
                  alive=self.alive
                 )