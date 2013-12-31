from yearplan import application
from flask import render_template
from api import AppView, AuthView , UserView, SheetView, EventView, common

#@application.route('/')
#def app_view():
#    return render_template('index.html')
    
AppView.register(application)
AuthView.register(application)
UserView.register(application)
SheetView.register(application)
EventView.register(application)

if __name__ == '__main__' :
   application.run(host='0.0.0.0', debug=True)
