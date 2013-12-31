from flask.ext.testing import TestCase
from apptest import AppTest
import json

class SheetTest(AppTest):
   
   sheet_fixture = dict(
         name = 'Developer Events',
         description ='stuff like hackathons and meetups ',
         location ='anywhere',
         phone = None,
         public = True,                        
         links = None,
         color = '#F0F0F0',
         tags = ['meetups', 'conferences', 'hackathons']
   )

   def test_index(self):
      # user who is not authenticated
      response = self.client.get('/sheet/',
                                 headers={'Content-Type':'application/json'})
      self.assert401(response)
      
      # valid user
      self.app_headers['X-yearplan-user'] = self.authenticateUser( guido )
      
      response2 = self.client.get('/sheet/', headers= self.app_headers)
      
      self.assert200(response2)
      self.assertIsNotNone( response2.json['objects'])
      self.assertTrue( response2.json['ok'] )
      
   def test_creating_and_then_retrieving_a_sheet(self):
        user_fixture = dict(
            name="James"
            email= "guido.van.awesome@python.org",
            password="lovesMontyPython",
            description="Python",
            links=[],
            location="Dropbox",
            phone="0800-AWESOME"
        )
        response1 = self.client.post('/user/',
                                data=json.dumps( user_fixture ),
                                headers=self.app_headers )
        self.assert201( response1 )
        self.assertIsNotNone( response1.json['objects'] )
        self.assertGreaterThan(1, len(response1.json['objects'][0]['uri']) )
        
        user_fixture['api_token'] = self.authenticateUser(user_fixture)


        sheet_fixture = dict(
            name = 'Developer Events',
            description ='stuff like hackathons and meetups ',
            location ='anywhere',
            phone = None,
            public = True,                        
            links = None,
            color = '#F0F0F0',
            tags = ['meetups', 'conferences', 'hackathons']
        )
        
        res1 = self.client.post('/sheet/', 
                        data=json.dumps(sheet_fixture),
                        headers = {
                            'Content-Type' : 'application/json',
                            'X-yearplan-user' : user_fixture['api_token']
                            }
                        )
        self.assertIsNotNone(res1.json.get('objects', None))
        self.assertGreaterThan(1, len(response1.json['objects']))
        self.assertIsNotNone(res1.json['objects'][0]['uri'])

        
        retrieve = self.client.post(obj['uri'], 
                        headers = {
                            'Content-Type' : 'application/json',
                            'X-yearplan-user' : user_fixture['api_token']
                            }
                        )
        obj = retrieve.json['objects'][0]
        
        self.assertIsNotNone(obj.get('uri', None))
        self.assertEqual(sheet_fixture['name'], obj['name'])
        self.assertEqual(sheet_fixture['description'], obj['description'])
        self.assertEqual(sheet_fixture['tags'], obj['tags'])

    def test_updating_details_of_sheet(self):
        pass
      
    def test_deleting_a_sheet(self):
        pass

    def test_adding_sheet_users(self):
        pass
   
    def test_updating_a_users_sheet_preferences(self):
        pass
   
    def test_retrieving_trashed_sheets(self):
        pass
   
    def test_retrieving_a_sheets_events(self):
        pass
   
    def test_sheet_event_trash(self):
        pass

