from flask import Flask
#from flask.ext.mongoengine import MongoEngine

application = Flask(__name__)
application.name = 'yearplanco'

application.config['MONGODB_SETTINGS'] = {'DB' : 'yearplanco' }
application.config['SECRET_KEY'] = '79656172506c616e434f415049'

#db = MongoEngine( app )

from routes import *

if __name__ == '__main__' :
   application.run(debug=True)