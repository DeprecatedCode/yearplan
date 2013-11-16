# -*- coding utf-8 -*-
from flask.ext.testing import TestCase
from user_test_data import *
import json
import unittest

class AppTest(TestCase):
   
   def create_app(self):
      from runserver import application
      return application
      
   def test_user_and_auth(self):
   
      # Get a list of users
      response =  self.client.get('/user/')
      self.assert200(response)
      
      # Create a User
      response = self.client.post('/user/',
                                 data=json.dumps(guido),
                                 headers={'Content-Type':'application/json'}
      )
      
      self.assertStatus(response, 201)
      
      self.assertIn('objects',response.json )
      # make sure we got the users record in the objects property
      self.assertEqual( len(response.json['objects']), 1 )
      
      rv = response.json.get('objects')
      
      data = rv[0]

      self.assertEqual( guido['name'], data['name'])
      self.assertEqual( guido['description'], data['description'] )
      self.assertEqual( guido['email'], data['email'])
      self.assertIsNotNone( data['uri'])
      # set the Uri for further requests
      guido['uri'] = data['uri']
      
      # Check if created user can be queried from given uri
      response =  self.client.get( guido['uri'] )
      self.assertStatus( response, 200 )
      
      # Try to get auth status, expect 401
      auth_response = self.client.get('/auth/')
      self.assert401( auth_response )
      
      
      self.assertFalse( auth_response.json['ok'] )
      
      # send proper auth details
      auth_response2 = self.client.post('/auth/',
                                       data=json.dumps(guido),
                                       headers={'Content-Type':'application/json'}
                                      )
      self.assert200( auth_response2 )
      
      print auth_response2.headers
      
      guido['api_token'] = auth_response2.headers.get('x-yearplan-user')
      
      self.assertIsNotNone( guido['api_token'] )
     
      
      self.assertEquals(dict(ok=True), auth_response2.json )
     
      # should now return 200
      auth_response = self.client.get('/auth/',
                                      headers={'x-yearplan-user': guido['api_token']}
                                     )
      self.assert200( auth_response )
   
   
if __name__ == '__main__' :
   unittest.main()