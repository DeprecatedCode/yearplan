from flask.ext.testing import TestCase
from apptest import AppTest
from data.user_test_data import *
import json

class AuthTest(AppTest):
   
   
   def test_get(self):
      # Try to get auth status, expect 401
      auth_response = self.client.get('/auth/')
      self.assert401( auth_response )
      self.assertFalse( auth_response.json['ok'] )
      
      
      auth_response2 = self.client.post('/auth/',
                                      data=json.dumps(guido),
                                      headers={'Content-Type':'application/json'}
      )
      guido['api_token'] = auth_response2.headers.get('x-yearplan-user')
      # should now return 200
      auth_response = self.client.get('/auth/',
                                      headers={'x-yearplan-user': guido['api_token']}
                                     )
      self.assert200( auth_response )
      
   def test_post(self):
      auth_response = self.client.get('/auth/')
      self.assert401( auth_response )
      
      
      self.assertFalse( auth_response.json['ok'] )
      
      # send proper auth details
      auth_response2 = self.client.post('/auth/',
                                       data=json.dumps(guido),
                                       headers={'Content-Type':'application/json'}
                                      )
      self.assert200( auth_response2 )
      
      guido['api_token'] = auth_response2.headers.get('x-yearplan-user')
      
      self.assertIsNotNone( guido['api_token'] )
      self.assertGreater( len(guido['api_token']), 1 )

      self.assertEquals(dict(ok=True), auth_response2.json )
     
      # should now return 200
      auth_response = self.client.get('/auth/',
                                      headers={'x-yearplan-user': guido['api_token']}
                                     )
      self.assert200( auth_response )
      
   def test_delete(self):

      self.test_get()
      print( guido )
      # should now return 200
      auth_response = self.client.delete('/auth/',
                                      headers={'x-yearplan-user': guido['api_token']}
                                     )
      self.assert200( auth_response )
      self.assertTrue( auth_response.json['ok'] )
   