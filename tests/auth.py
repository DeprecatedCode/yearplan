from flask.ext.testing import TestCase
from apptest import AppTest
import json

class AuthTest(AppTest):
   
    fixture = dict( name="Peter Parker",
        email= "peter@spiderman.org",
        password="marryJane<3",
        description="Spiderman",
        links=['http://marvel.com/comics/spiderman'],
        location="",
        phone=""
    )
    
    user_created = False
    def create_user(self):
        if self.user_created :
            return
        
        resp = self.client.post('/user/',
            data = json.dumps(self.fixture),
            headers={'Content-Type':'application/json'}
        )

        self.assertTrue(resp.json['ok'])
        self.user_created = resp.json['ok']
        
        self.assertIsNotNone(resp.json['objects'])
        self.assertEqual(len(resp.json['objects']), 1)
        self.assertIn('email', resp.json['objects'][0])
        self.assertEqual(resp.json['objects'][0]['email'], self.fixture['email'])
        
    def test_retrieving_authentication_status(self):
        # Try to get auth status, expect 401
        auth_response = self.client.get('/auth/')
        self.assert401( auth_response )
        self.assertFalse( auth_response.json['ok'] )


        auth_response2 = self.client.post('/auth/',
                                      data=json.dumps(self.fixture),
                                      headers={'Content-Type':'application/json'}
        )
        self.fixture['api_token'] = auth_response2.headers.get('X-yearplan-user',None)
        
        self.assertIsNotNone(self.fixture['api_token']) 
        # should now return 200
        response = self.client.get('/auth/',
                            headers={
                                'X-yearplan-user': self.fixture['api_token']
                            }
        )
        self.assert200( response )
      
    def test_authenticating_into_the_api(self):
        self.create_user()
        
        auth_response = self.client.get('/auth/')
        self.assert401( auth_response )
           
        self.assertFalse( auth_response.json['ok'] )

        # send proper auth details
        auth_response2 = self.client.post('/auth/',
                            data = json.dumps(self.fixture),
                            headers = { 'Content-Type' : 'application/json' }
        )
        
        self.assert200(auth_response2)
        self.fixture['api_token'] = auth_response2.headers.get('X-yearplan-user')

        self.assertIsNotNone( self.fixture['api_token'] )
        self.assertGreater( len(self.fixture['api_token']), 1 )

        self.assertEquals(dict(ok=True), auth_response2.json )

        # should now return 200
        auth_response = self.client.get('/auth/',
                                      headers={
                                      'X-yearplan-user': self.fixture['api_token']}
                                     )
        self.assert200( auth_response )

        def test_closing_an_auth_session():
            self.fixture['api_token'] = self.authenticateUser(self.fixture)
            
            auth_response = self.client.delete('/auth/',
                                headers={
                                    'X-yearplan-user': self.fixture['api_token']
                                }
            )
            
            self.assert200(auth_response)
            self.assertTrue(auth_response.json['ok'])
            
        test_closing_an_auth_session()
   