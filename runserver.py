from yearplan import application
from api import AppView, AuthView , UserView, SheetView, EventView, common
   
AppView.register(application)
AuthView.register(application)
UserView.register(application)
SheetView.register(application)
EventView.register(application)

if __name__ == '__main__' :
   application.run(host='0.0.0.0', debug=False)
