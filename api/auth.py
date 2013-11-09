# -*- coding utf-8 -*-
from flask import request, g, abort, url_for, jsonify, session, after_this_request
from flask.ext.classy import FlaskView
from models import Auth, User, Session
from common import require_auth

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
