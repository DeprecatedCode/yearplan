from flask import request, g, abort, url_for, jsonify, session, after_this_request
from flask.ext.classy import FlaskView
from yearplan import application
from models import Auth, User, Sheet, UserSheet
from common import require_auth

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