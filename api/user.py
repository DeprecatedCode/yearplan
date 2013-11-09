from flask import request, g, abort, url_for, jsonify, session
from flask.ext.classy import FlaskView
from common import require_auth
from models import User, Auth, Event, Session

class UserView(FlaskView):

   # /user/
   def index(self):
      dbusers = User.objects.all()
      
      _users = [ user.__dict__() for user in dbusers ]
      
      return jsonify(ok=True, objects=_users), 200

   def get(self, id=None):
      _user = User.objects.get_or_404( id = id )
      return jsonify( ok=True, objects=[_user.__dict__()] ),200
      
      
   def post(self):
      #return jsonify(data=request.json),200
      if not request.json or 'name' not in request.json :
         abort(400)
         
      new_user = User(
                      name= request.json['name'],
                      email= request.json['email'],
                      alive=False,
                      public=False)

      new_user.save()

      if 'password' in request.json :
         auth = Auth( user= new_user, password = request.json['password'] )
         auth.save()
      
      return jsonify(ok=True), 201
         
      abort(404)    

   @require_auth  
   def put(self, id=None):
      abort(501)
      
      if 'user' in request.json:
         # save the old details in history
         abort(401)

   @require_auth
   def event(self, id ):
      abort(501)
      #if 'from' not in or 'to' not in request.args:
      #   abort(400, error = 'missing arguments from and to ') bad request
      #_user = User.objects.get_or_404()
      #_events = [ event.__dict__() for event in Event.objects.all( user = _user ) ]