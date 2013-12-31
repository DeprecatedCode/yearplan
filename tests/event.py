from flask.ext.testing import TestCase
from apptest import AppTest
import json
from datetime import date

class EventTest(AppTest):
   
    user_fixtures = (
        dict( name="James"
            email= "guido.van.awesome@python.org",
            password="lovesMontyPython",
            description="Python",
            links=[],
            location="Dropbox",
            phone="0800-AWESOME"
        ),            
        dict( name="John e. Rezig",
            email= "ejohn@jquery.org",
            password="$.('#teach>.your').children('.toCode')",
            description="Originator of the JQuery Machine",
            links=[],
            location="Khan Academy",
            phone="0800-AWESOME"
        )
    )
   
    def setup():
      # create the users and the sheets
        response1 = self.client.post('/user/',
                                data=json.dumps( user_fixtures[0] ),
                                headers=self.app_headers )
        self.assert201( response1 )
        self.assertIsNotNone( response1.json['objects'] )
        self.assertGreaterThan(1, len(response1.json['objects'][0]['uri']) )
      
        user_fixtures[0]['uri'] = response1.json['objects'][0]['uri']
      
        response2 = self.client.post('/user/',
                             data=json.dumps( user_fixtures[1] ),
                             headers=self.app_headers )
      
        self.assert201( response2 )
        user_fixtures[1]['uri'] = response2.json['objects'][0]['uri']
      
      
      
    def test_creating_a_sheet_and_adding_an_event(self):
        # /event/:id
        user_fixture = user_fixtures[0]
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
        
        event = dict(
            name = 'Python Conference',
            dates = ['2014-01-01'],
            event_date = '2014-01-01',
            description = 'Greatest python conference of all time ?',
            location = 'London, England',
            public = True,
            links = ['http://pyconf.eu']
            color = ''
            tags = ['python', 'programming', 'conferences', 'hackerthon']
        )
        
        res1 = self.client.post('/sheet/', 
                        data=json.dumps(sheet_fixture),
                        headers = {
                            'Content-Type' : 'application/json',
                            'X-yearplan-user' : user_fixture['api_token']
                            }
                        )
        self.assertIsNotNone(res1.json.get('objects', None))
 
        
        sheet_fixture = res1.json['objects'][0]
        
        event_resp1 = self.client.post( '%s/events' % sheet_fixture['uri'], 
                        data=json.dumps(event),
                        headers = {
                            'Content-Type' : 'application/json',
                            'X-yearplan-user' : user_fixture['api_token']
                            }
                        )
        self.assertIsNotNone(res1.json.get('objects', None))
        
    def test_updating_an_events_details(self):
        pass

    def test_deleting_an_event(self):
      pass
      
    def test_moving_an_event_to_another_sheet(self):
        # /event/move/:id?from=X&to=Y
        pass
      
    def test_getting_alist_of_trashed_events(self):
        # sheet/:id/event/trash      
        pass