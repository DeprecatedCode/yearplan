# -*- coding utf-8 -*-

from main import application
from model import *
from flask import request, g, abort, url_for, jsonify, session, after_this_request
from flask.ext.classy import FlaskView
import itsdangerous as security

@application.errorhandler(404)
def resource_not_found(error):
   return jsonify(ok=False, errors= ['Not found']), 404

@application.errorhandler(401)
def not_authorised(error):
   return jsonify(ok=False,errors=['Not authorised']), 401

@application.errorhandler(400)
def bad_request(error):
   return jsonify(ok=False, errors= ['Bad Request.']), 400

@application.errorhandler(501)
def not_implemented(error):
   return jsonify(ok=False, errors=['Not yet available in this version of the API']),501

def require_auth(f):
   def decorator( *args, **kwargs ):
      if 'yearplan_user' not in session:
         abort( 401 )
      
      return f( *args, **kwargs )
   return decorator

class AuthView(FlaskView):


   @require_auth
   def index(self):
      return jsonify(ok=True), 200
   
   def post(self):
      if 'email' not in request.json or 'password' not in request.json :
         abort(400)
      
      try:   
         ''' check authentication '''
         auth  = Auth.objects.get(password=request.json['password'],
                                 user= User.objects.get(email=request.json['email']).id,
                                 alive=False )
      except (MultipleObjectsReturned, DoesNotExist, ValidationError):
         abort(401)
      
      _session = Session(auth_id= str(auth.id))
      _session.save()
      ''' setup a new session '''
      auth.sessions.append( _session )
      auth.update(upsert=False,**{ 'set__hash': str(auth.id) + str(_session.id)})
      ''' set a cookie for the client '''
      session['user'] = str(auth.user.id)
      session['yearplan_user'] = str(auth.id) + str(_session.id)
      @after_this_request
      def add_header( response ):
         response.headers['x-yearplan-user'] = session['yearplan_user']
         return response
      
      return jsonify(ok=True), 200
      abort(401)

   @require_auth
   def delete(self):
      if 'yearplan_user' in session:
         del session['user']
         del session['yearplan_user']
         
      return jsonify(ok=True,msg= ['Session ended']),200

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

class SheetView(FlaskView):

   decorators = [ require_auth ]
   
   def index(self, id=None):
      abort(501)

   def get(self, id):
      abort(501)

   def post(self):
      abort(501)

   def put(self, id):
      abort(501)

   def delete(self, id):
      abort(501)

   # add user to a sheet
   def users(self, id, user_id ):
      abort(501)

   # POST
   def event(self, id):
      abort(501)

   # /sheet/trash
   def trash(self):
      """Recently deleted sheets within past 24hrs"""
      abort(501)

   @application.route('/sheet/<int:id>/events/trash')
   def event_trash(self, id):
      """ recently deleted events, within the last 24 hrs """
      abort(501)
   @application.route('/sheet/:id/users/:user_id', methods = ['PUT', 'GET'])	
   def preferences(self, id, user_id):
      abort(501)

class EventView(FlaskView):
   
   decorators = [ require_auth ]
   
   def index(self):
      """ Get all events for logged in user """
      abort(501)

   def get(self, id):
      return abort(501)

   def post(self, id):
      abort(501)

   
   def delete(self, id):
      abort(501)

   def put(self, id):
      """ Get an events detailes, Edit and/or delete an event"""
      abort(501)

   def trash(self):
      """ trashed events """
      abort(501)

AuthView.register(application)
SheetView.register(application)
EventView.register(application)
UserView.register(application)
