# -*- coding utf-8 -*-
from flask.ext.testing import TestCase
import unittest
import json

class AppTest(TestCase):
   
   app_headers = { 
                  'Content-type' : 'application/json'
                  #'x-yearplan-user' : ''
              }
   def create_app(self):
      from runserver import application
      return application

   def assert201( self, response ):
      self.assertStatus( response, 201 )

   def assert400( self, response ):
      self.assertStatus(response, 400)
      
   def authenticateUser(self, user):
      auth_response = self.client.post('/auth/',
                                      data=json.dumps(user),
                                      headers={'Content-Type':'application/json'}
      )
      
      self.assert200( auth_response )
      user['api_token'] = auth_response.headers.get('x-yearplan-user')
      return user['api_token']