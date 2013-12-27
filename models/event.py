from yearplan import db
from entity import Entity
from flask import url_for
from models import Sheet

class Event (Entity, db.Document):
    event_date = db.DateTimeField()
    dates = db.ListField( db.DateTimeField() )
    sheet = db.ReferenceField(Sheet)
    
    def to_json(self): 
       return dict(
                id=str(self.id),
                uri=url_for('EventView:get',id= str(self.id)),
                sheet=self.sheet.to_json().uri,
                name=self.name,
                description=self.description,
                event_date=self.event_date,
                dates=self.dates,
                location=self.location,
                links=self.links,
                color=self.color,
                public=self.public
                )

