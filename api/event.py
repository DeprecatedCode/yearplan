from flask import request, g, abort, url_for, jsonify, session, after_this_request
from flask.ext.classy import FlaskView
from models import Auth, User, Event
from common import require_auth

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