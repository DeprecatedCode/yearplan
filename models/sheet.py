from yearplan import db
from entity import Entity
from user import User
from flask import url_for

class Sheet (Entity, db.Document):
    created_by = db.ReferenceField(User)
    
    def to_json(self): 
        return dict(
                id=str(self.id),
                uri=url_for('SheetView:get',id= str(self.id)),
                name=self.name,
                description=self.description,
                links=self.links,
                color=self.color,
                public=self.public,
                created_by=url_for('UserView:get', id=str(self.created_by))
                )