from flask import Flask
from flask.ext.mongoengine import MongoEngine
application = Flask(__name__)
application.name = 'yearplanco'

application.config['MONGODB_SETTINGS'] = {'DB' : 'yearplan' }
application.config['SECRET_KEY'] = 'bf8df11aecf7d514713596c62afc8e2d242e0f66e16cb'
app_salt = application.config['SECRET_KEY']

db = MongoEngine( application )