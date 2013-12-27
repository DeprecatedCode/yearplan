from yearplan import db
from entity import Entity
from user import User
from sheet import Sheet
from flask import url_for
from datetime import datetime

class UserSheet (Entity, db.Document):
    sheet = db.ReferenceField(Sheet)
    user = db.ReferenceField(User)
    starred = db.BooleanField(default=False)
   
    @staticmethod
    def deleteSheet (aSheet):
        try:
            user_sheets = UserSheet.get(sheet=aSheet, alive=True)
        except: 
            return False
        
        for x in user_sheets :
            x.alive = False
            x.updated_at = datetime.now()
            x.history.append( x )
            x.save()
        return True

    def to_json(self): 
        return dict(
                    id=str(self.sheet.id),
                    uri=url_for('SheetView:get',id= str(self.sheet.id)),
                    name=self.sheet.name,
                    description=self.sheet.description,
                    links=self.sheet.links,
                    color=self.sheet.color,
                    public=self.public,
                    starred=self.starred,
                    created_by=self.sheet.created_by
                    )