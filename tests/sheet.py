from flask.ext.testing import TestCase
from apptest import AppTest
from data.user_test_data import * 
import json

class SheetTest(AppTest):
   
   def test_index(self):
      # user who is not authenticated
      response = self.client.get('/sheet/',headers=self.app_headers)
      
      self.assert401(response)
      
      # valid user
      guido['api_token'] = self.authenticateUser( guido )
      
      self.app_headers['x-yearplan-user'] =  guido['api_token']
      
      response = self.client.get('/sheet/', headers= self.app_headers)
      
      self.assert200(response)
      self.assertIsNotNone( response.json['objects'])
      self.assertTrue( response.json['ok'] )
      
   def test_get(self):
      
      # Unauthenticated user
      response = self.client.get('/sheet/<id>')
      
      self.assert401(response)
      
      self.app_headers['x-yearplan-user'] = self.authenticateUser( guido )
      
      response = self.client.get('/sheet/<id>', headers=self.app_headers)
      
      self.assert200(response)
      self.assertIsNotNone(response.json['objects'])
      self.assertTrue(response.json['ok'])
      
   def test_post(self):
      
      response = self.client.post('/sheet/')
      
      self.assert401(response)
      
      self.assertFalse( response.json['ok'])
      
      self.app_headers['x-yearplan-user'] = self.authenticateUser( guido )

      response = self.client.post('/sheet/', headers=self.app_headers)

      self.assert201( response )
      self.assertIsNotNone(response.json['objects'])
      self.assertTrue(response.json['ok'])
      respData = response.json['objects'][0]
      
      self.assertEquals( data['title'], respData['title'])
      self.assertEquals( data['title'], respData['title'])
      
      self.assertIsNotNone( respData['uri'] )
      
      self.assert200( self.client.get( respData['uri'],headers=self.app_headers))

   def test_put(self):
      test_data= dict()
      
      response = self.client.put('/sheet/:id', data=test_data)
      
      self.assert401(response)
      
      self.assertFalse( response.json['ok'])
      

      response = self.client.put('/sheet/:id', headers=self.app_headers)
      
      self.assert200( response )
      
      response = self.client.get( test_data['uri'],headers=valid_headers)
      
      self.assertIsNotNone(response.json['objects'])
      
      self.assertTrue(response.json['ok'])
      respData = response.json['objects'][0]
      
      self.assertEquals( test_data['title'], respData['title'])
      self.assertEquals( test_data['title'], respData['title'])
      self.assertEquals( test_data['uri'], respData['uri'])
      
   def test_delete(self):
      self.app_headers['x-yearplan-user'] = self.authenticateUser( guido )
      response = self.client.delete('/sheet/:id')
      
      self.assert200(response)

   def test_add_sheet_users(self):
      pass
   
   def test_preferences(self):
      pass
   
   def test_sheet_events(self):
      pass
   
   def test_sheet_trash(self):
      pass
   
   def test_sheet_event_trash(self):
      pass

