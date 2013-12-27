from yearplan import db, app_salt
from .base import BaseModel
from .user import User
from flask import request
import hashlib

class Auth (BaseModel, db.Document):
    
    user = db.ReferenceField(User)
    sessions = db.ListField()
    password = db.StringField(max_length=255)
    hash = db.StringField()
    
    ''' 
    leaving the collection name as `auth` conflicts with mongos db.auth() stuff    
    '''
    meta = {
        'collection' : 'yearplan_auth'
    }
    
    @staticmethod
    def hash_password(email, password ):
        _hashed = hashlib.md5(email.lower() + password + app_salt)
        return _hashed.hexdigest()

    @staticmethod
    def getUser ():
        user_token = request.headers['X-yearplan-user']
        user_auth = Auth.objects.get(hash=user_token)
        return user_auth.user

