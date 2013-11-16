from flask import session, abort, jsonify
from yearplan import application
from api import AuthView , UserView, SheetView, EventView, common

@application.errorhandler(400)
def bad_request(error):
   return jsonify(ok=False, errors= ['Bad Request.']), 400

@application.errorhandler(401)
def not_authorised(error):
   return jsonify(ok=False,errors=['Not authorised']), 401

@application.errorhandler(404)
def resource_not_found(error):
   return jsonify(ok=False, errors= ['Not found']), 404
   
@application.errorhandler(405)
def method_not_allowed(error):
   return jsonify(ok=False, errors= ['Method Not allowed']), 405
   
@application.errorhandler(410)
def resource_gone(error):
   return jsonify(ok=False, errors= ['Resource deleted']), 410

@application.errorhandler(501)
def not_implemented(error):
   return jsonify(ok=False, errors=['Not yet available in this version of the API']),501
   
AuthView.register(application)
UserView.register(application)
SheetView.register(application)
EventView.register(application)

if __name__ == '__main__' :
   application.run(debug=True)