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
                  uri=url_for('SheetView:get',id= str(self.sheet.id)),
                  public=self.sheet.public,
                  starred=self.starred,
                  alive=self.alive
                 )