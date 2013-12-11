from flask.ext.testing import TestCase
from apptest import AppTest
from data.user_test_data import *
import json

class UserTest(AppTest):

   def test_index(self):
      # Get a list of users
      response =  self.client.get('/user/')
      self.assert200(response)
      
      
   def test_get(self):
      pass
   def test_post(self):
      
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
      

   
   def test_put(self):
      pass
   def test_delete(self):
      pass
   def test_user_events(self):
      pass
   def test_user_sheet(self):
      pass
