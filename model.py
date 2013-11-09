# models
from main import db
from datetime import datetime
from flask import url_for

class BaseModel( db.Document):
   created_at = db.DateTimeField(default=datetime.now, required=True)
   updated_at = db.DateTimeField(default=datetime.now, required=True)
   alive = db.BooleanField(default=False, required=True)
   history = db.ListField()
   
   meta = {
			  'allow_inheritance' : True ,
			  'indexes' : ['-created_at', 'alive'],
			  'ordering': ['-created_at']
	}


class Entity(BaseModel):
   name = db.StringField( required=True)
   description = db.StringField(max_length=300 )
   location = db.StringField(max_length=255 )
   phone = db.StringField(max_length=50 )
   public = db.BooleanField()
   created_by = db.StringField()
   links = db.ListField( db.StringField())
   color = db.StringField()
   tags = db.ListField( db.EmbeddedDocumentField('Tag') )

class User( Entity ):
   email = db.StringField()
   
   def __dict__(self):
      return {
            #'id' : self.id.__str__(),
            'name' : self.name,
            'email': self.email,
            'uri' : url_for('UserView:get',id= self.id.__str__())
         }
class Sheet(Entity):
   created_by = db.ReferenceField(User)
   
class UserSheet( Entity ):
   sheet = db.ReferenceField(Sheet)
   user = db.ReferenceField( User )
   starred = db.BooleanField(default=False)

class Event(Entity):
   dates = db.ListField( db.DateTimeField() )
  
class Tag( Entity ):
   pass 

class Session(BaseModel):
   auth_id = db.StringField()
	
class Auth(BaseModel):
   user = db.ReferenceField(User)
   sessions = db.ListField( )
   password = db.StringField(max_length=255)
   # hash -> auth_id + session_id 
   hash = db.StringField()