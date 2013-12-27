from yearplan import db
from flask import url_for
from .entity import Entity

class User (Entity, db.Document):
    email = db.StringField()
    phone = db.StringField(max_length=50)
    
    def to_json(self):
        return dict(
                id=str(self.id),
                uri=url_for('UserView:get', id=str(self.id)),
                name=self.name,
                email=self.email,
                description=self.description,
                location=self.location,
                phone=self.phone,
                links=self.links,
                public=self.public
                )

                