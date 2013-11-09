from yearplan import db
from datetime import datetime

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

