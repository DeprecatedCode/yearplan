from flask import request, g, abort, url_for, jsonify, session
from flask.ext.classy import FlaskView,route
from common import require_auth
from models import User, Auth, Event, UserSheet
from datetime import date, timedelta
from flask_cors import cross_origin

class UserView (FlaskView):
    decorators = [ cross_origin(origins='*',automatic_options=True) ]
    def index(self):
        users = User.objects(alive=True)
        
        return jsonify(ok=True, objects=[u.to_json() for u in users]), 200

    def get(self, id):
        user = User.objects.get_or_404(id=id, alive=True )
        
        return jsonify( ok=True, objects=[user.to_json()] ), 200

    def post(self):
        if not request.json or 'name' not in request.json :
            abort(400)
        
        user = User.objects(email= request.json['email'])
        if len(user) > 0 :
            return jsonify(
                        ok=False,
                        errors=['Email already in use. Account creation failed']
                        ), 403
        
        new_user = User(name= request.json['name'],
                        email= request.json['email'],
                        alive=True
                        )
        
        new_user.description = request.json.get('description', None )
        new_user.location = request.json.get('location', None )
        new_user.phone = request.json.get('phone', None )
        new_user.public = True
        
        new_user.save()
        
        if 'password' in request.json :
            auth = Auth( user= new_user, password=request.json['password'], alive=False )
            
            auth.password = auth.hash_password(
                                    request.json['email'],
                                    request.json['password'])
            auth.save()
        
        return jsonify(ok=True, objects=[new_user.to_json()]), 201

    @require_auth  
    def put(self, id):
        """ Update a user's details """
        user = User.objects.get_or_404(id=id)
        #prevent non authorised users from editing other user's details
        _currentUser = Auth.getUser()
        
        if _currentUser != user :
            abort(401)
            
        if 'user' in request.json:
            # save the old details in history
            user.history.append( user )
            
            user.name = request.json['user']['name']
            user.description = request.json['user']['description']
            user.location = request.json['user']['location']
            user.phone = request.json['user']['phone']
            user.links = request.json['user'].get('links', [])
            user.alive = True
            user.save()
            
            # create an Auth account if it doesn't exist or
            # update the password if it does
            if 'password' in request.json['user'] :
                try:
                    auth = Auth.objects.get(user=user)
                except(Exception):
                    auth = Auth(user=user,
                                password=request.json['user']['password'],
                                alive=True
                                )
                
                auth.password = Auth.hash_password(user.email, auth.password)
                
                auth.save()
            
            return jsonify(ok=True),200
        abort(401)

    @require_auth
    def delete(self,id):
        """ Delete a user account """ 
        user = User.objects.get_or_404(id=id)
        user.history.append(user)
        user.alive = False
        user.save()
        return jsonify(ok=True),200

    @require_auth
    @route('/<string:id>/events', methods=['GET'])
    def event(self, id ):
        """ Show the current user's events from all connected sheets """
        user = User.objects.get_or_404(id=id, alive=True)
        
        date_from = request.args.get('from', None)
        date_to = request.args.get('to',None)
      
        if (date_from is None or date_to is None  ):
            abort(400)
        
        # Get all the sheet's the user is connected to
        users_sheets = UserSheet.objects(user=user, alive=True)
        
        all_events = []
        events = []
        # foreach connected sheet, get the associated events
        for sheet in users_sheets:
            #add the event to the list of events
            for event in Event.objects(sheet=sheet, alive=True):
                all_events.append( event )
            
        isWithin = lambda frm, to, val: (val >= frm and val <= to)
      
        for event in all_events :
            if isWithin(date_from, date_to, event.event_date) :
                events.append( event.to_json() )
        
        return jsonify(ok=True, objects=events)

    @require_auth
    def profile(self):
        ''' get the profile of the currently authenticated user '''
        try:
            user = Auth.getUser() # @Todo rename this to getLoggedInUser()
            return jsonify(ok=True, objects=[user.to_json()]), 200
        except:
            # @Todo
            pass
        abort(500)