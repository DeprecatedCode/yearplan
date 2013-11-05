# -*- coding utf-8 -*-
# authenticated_cookies
# e.g. yearplan_user=7bc60c92213611c835311aab9df76909
from main import application
from flask import request, g, abort, url_for, make_response
from flask.ext.classy import FlaskView

@application.errorhandler(404)
def resource_not_found(error):
   return "Not found", 404

@application.errorhandler(401)
def not_authorised(error):
   return 'Not authorised', 401
   
@application.errorhandler(501)
def not_implemented(error):
   return 'not yet available in this version of the API',501
#Auth API


class AuthView(FlaskView):

   #@application.route('/auth', methods = ['GET', 'POST', 'DELETE'])
   def index(self):
      abort(501)
      
   def post(self):
      abort(501)
      
class UserView(FlaskView):

   # /user/:id
   def index(self):
      abort(501)

   def get(self, id=None):
      abort(501)
      
   def put(self, id=None):
      abort(501)
      
   def event(self, id ):
      abort(501)
      
class SheetView(FlaskView):

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
