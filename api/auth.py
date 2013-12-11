# -*- coding utf-8 -*-
from flask import request, g, abort, url_for, jsonify, session, after_this_request, make_response
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
       
      ''' check authentication '''
      # was using  user Id to pull the user info
      user = User.objects.get_or_404(email=request.json['email'])
      
      _password = Auth.hash_password(request.json['email'], request.json['password'])
      
      auth = Auth.objects.get_or_404(user=user,password=_password, alive=True )
      
      _session = Session(auth_id=str(auth.id),alive=True)
      _session.save()
      ''' setup a new session '''
      auth.sessions.append( _session )
      auth.alive = True
      auth.hash = str(auth.id) + str(_session.id)
      auth.save()
      
      session.yearplan_user = str(auth.id) + str(_session.id)

      response = make_response( jsonify(ok=True), 200 )
      response.set_cookie('yearplan_user',value=auth.hash)
      response.headers['x-yearplan-user'] = auth.hash
      
      return response

   @require_auth
   def delete(self):
      if 'x-yearplan-user' in request.headers:
         try:
            auth = Auth.objects.get(hash=request.headers['x-yearplan-user'])
            auth.history.append(auth)
            auth.hash = None
            auth.save()
            auth.alive = False
            del session['user']
            del session['yearplan_user']
         except:
            pass
      return jsonify(ok=True),200
