# -*- coding utf-8 -*-
from flask import (request, g, abort, url_for, jsonify,
                    session, after_this_request, make_response)
from flask.ext.classy import FlaskView
from models import Auth, User, Session
from common import require_auth

class AuthView (FlaskView):

    @require_auth
    def index (self):
        return jsonify(ok=True), 200
    
    def post (self):
        if not request.json :
            abort(400)
        
        email = request.json.get('email', None)
        password = request.json.get('password', None)

        if email == None or password == None :
            abort(400)
        
        ''' check authentication '''
        try:
            user = User.objects.get(email=email)
            password = Auth.hash_password(user.email, password)
        
            auth = Auth.objects.get(user=user, password=password)
            
            ''' setup a new session '''
            _session = Session(auth_id=str(auth.id),alive=True)
            _session.save()
        
            auth.sessions.append( _session )
            auth.alive = True
            auth.hash = str(auth.id) + str(_session.id)
            auth.save()

            response = make_response(jsonify(ok=True), 200 )
            response.set_cookie('yearplan_user', value=auth.hash)
            response.headers['X-yearplan-user'] = auth.hash
            
            return response
                
        except:
            pass
            
        abort(401)    
    @require_auth
    def delete (self):
        api_token = request.headers.get('X-yearplan-user', None)
        if api_token != None:
            try:
                auth = Auth.objects.get(hash=api_token)
                auth.history.append(auth)
                auth.hash = None
                auth.alive = False
                auth.save()
            except:
                pass
        return jsonify(ok=True), 200

