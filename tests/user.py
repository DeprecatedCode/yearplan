from flask.ext.testing import TestCase
from apptest import AppTest
import json

class UserTest(AppTest):
    
    def test_index(self):
        response =  self.client.get('/user/')
        self.assert200(response)
        self.assertTrue(response.json['ok'])
        
    def test_creating_users(self):
        # create some users that will be used in the application
        
        fixtures = tuple([
            dict( name="Guido V. Awesome",
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
            ),
            dict( name="Chuck Norris",
                email= "chuck@org.gov.com.net",
                password="c_h_u_c_k",
                description="It's Chuck Norris. Run.",
                links=[],
                location="USA",
                phone="0800-AWESOME"
            )
        ])
        for user in fixtures:
            response = self.client.post('/user/',
                            data=json.dumps(user),
                            headers={'Content-Type':'application/json'}
            )
          
            self.assertStatus(response, 201)
          
            self.assertIn('objects',response.json )
            # make sure we got the user's record in the objects property
            self.assertEqual( len(response.json['objects']), 1 )
          
            respData = response.json.get('objects')
            respObj = respData[0]

            self.assertEqual(user['name'], respObj['name'])
            self.assertEqual(user['description'], respObj['description'] )
            self.assertEqual(user['email'], respObj['email'])
            self.assertIsNotNone( respObj['uri'])
            #check that the URI has the form /user/:id
            self.assertEqual(respObj['uri'], '/user/%s' % respObj['id'])
            
            # Check if created user can be queried from given uri
            response =  self.client.get( respObj['uri'] )
            self.assertStatus( response, 200 )
        
        response = self.client.get('/user/')
        
        self.assertTrue(response.json['ok'])
        self.assertEqual(len(response.json['objects']), 3)
        
    def test_getting_a_users_details(self):
        fixture = dict( name="Bob MacMillan",
            email= "robertmcmillan@mail.com",
            password="!robomi11@",
            description="Some guy named Bob",
            links=['http://mcmillan-bob.me/blog/'],
            location="Atlanta",
            phone=None
        )
        
        # create the users first
        resp = self.client.post('/user/',
                    data=json.dumps(fixture),
                    headers={'Content-Type':'application/json'}
        )
        self.assertTrue(resp.json['ok'])
        self.assertIsNotNone(resp.json['objects'])
        
        fixture['uri'] = resp.json['objects'][0]['uri']
        
        # create the users first
        getResp = self.client.get(fixture['uri'])
        
        self.assertTrue(getResp.json['ok'])
        self.assertIsNotNone(getResp.json['objects'])
        
        respObj = getResp.json['objects'][0]
        
        self.assertIn('uri', respObj)
        self.assertEqual(respObj['name'], fixture['name'])
        self.assertEqual(respObj['location'], fixture['location'])
        self.assertEqual(respObj['phone'], fixture['phone'])
        self.assertEqual(respObj['email'], fixture['email'])
        self.assertEqual(respObj['description'], fixture['description'])
        self.assertNotIn('password', respObj)


    def test_updating_users_information(self):
        '''
            Test the put method
        '''
        fixture = dict( name="Mario Lineman",
            email= "mario@quasimondo.com",
            password="hyp3r80lic!",
            description="Awesome Computer graphics guy!!",
            links=['http://quasimondo.com/lab'],
            location="Home",
            phone=""
        )
        # create the user first
        response = self.client.post('/user/',
                    data=json.dumps(fixture),
                    headers={
                        'Content-Type':'application/json'
                    }
        )
        
        self.assertIsNotNone(response.json.get('objects', None))
        self.assertEqual(len(response.json['objects']), 1)
        self.assertIsNotNone(response.json['objects'][0]['uri'])
        
        fixture['uri'] = response.json['objects'][0]['uri']
        #update the users info
        fixture['name'] = 'Mario X. Klingeman'
        fixture['links'].append('http://twitter.com/mklingeman/')

        # first try without auth header
        self.assert401( self.client.put(fixture['uri'],
                            data=json.dumps({ 'user' : fixture}),
                            headers={ 'Content-Type' : 'application/json' }
                        )
        )
        
        # Authenticated user
        fixture['api_token'] = self.authenticateUser(fixture)    
        
        resp2 = self.client.put(fixture['uri'],
                    data=json.dumps({ 'user' : fixture}),
                    headers={
                        'Content-Type' : 'application/json',
                        'X-yearplan-user' : fixture['api_token']
                    }
        )
        
        self.assert200(resp2)
        self.assertTrue(resp2.json['ok'])
    
    def test_updating_other_users_information_(self):
        '''
            Test updating user's information by another user
            
            users should not be able to change information that does not belong
            to them.
            i.e. a user should not be able to update another user's details
        '''
        fixtures = tuple([
            dict( name="Jack Smith",
                email= "jack@mail.com",
                password="jack290",
                description="Some guy named jack",
                links=['http://jack-is-myth.blogspot.com'],
                location="Lost forest",
                phone=""
            ),
            dict( name="Jane Doe",
                email= "jeniferd@janedoe.org",
                password="1@jane",
                description="Just being jane",
                links=[],
                location="",
                phone=""
            )
        ])
                
        for user in fixtures :
            # create the users first
            resp = self.client.post('/user/',
                        data=json.dumps(user),
                        headers={'Content-Type':'application/json'}
            )
            self.assertTrue(resp.json['ok'])
            self.assertIsNotNone(resp.json['objects'])
            self.assertEqual(len(resp.json['objects']), 1)
            # get the user's uri
            user['uri'] = resp.json['objects'][0]['uri']
        
            resp = self.client.get( user['uri'] )
            
            self.assertIsNotNone(resp.json['objects'])
            self.assertTrue(resp.json['ok'])
            self.assertEqual(resp.json['objects'][0]['name'], user['name'])
            self.assertEqual(resp.json['objects'][0]['location'], user['location'])
        
        self.assertIsNotNone(fixtures[0]['uri'])
        
        # login to the application as the first user     
        fixtures[0]['api_token'] = self.authenticateUser( fixtures[0])
        
        #update the other user's info
        fixtures[1]['phone'] = '0800-983-0202'
        fixtures[1]['links'].append('http://janedoe.livejournal.com/index.aspx')

        resp2 = self.client.put(fixtures[1]['uri'],
                    data=json.dumps({ 'user' : fixtures[1]}),
                    headers={
                        'Content-Type' : 'application/json',
                        'X-yearplan-user' : fixtures[0]['api_token']
                    }
        )
        
        self.assert401(resp2)
        self.assertFalse(resp2.json['ok'])
        
    def test_delete(self):
            
        fixture = dict( name="Jessie McCallaghan",
                email= "messyjessy@ymail.com",
                password="j355!emac",
                description="Messy jessy :P",
                links=['http://jessisamess.tumblr.com'],
                location="Clean room",
                phone=""
        )
        
        # create the users first
        resp = self.client.post('/user/',
                    data=json.dumps(fixture),
                    headers={'Content-Type':'application/json'}
        )
        self.assertTrue(resp.json['ok'])
        self.assertIsNotNone(resp.json['objects'])
        self.assertEqual(len(resp.json['objects']), 1)
        # get the user's uri
        fixture['uri'] = resp.json['objects'][0]['uri']
    
        # delete without authentication
        delete_resp = self.client.delete(fixture['uri'])
        
        self.assert401(delete_resp)
        self.assertFalse(delete_resp.json['ok'])

        fixture['api_token'] = self.authenticateUser(fixture)
        # delete with authentication
        delete_resp = self.client.delete(fixture['uri'], 
            headers = {
                'X-yearplan-user' : fixture['api_token']
            }
        )
        
        self.assert200(delete_resp)
        self.assertTrue(delete_resp.json['ok'])

    def test_user_events(self):
        return True
        
        fixture = dict( name="Jack Smith",
            email= "jack@mail.com",
            password="jack290",
            description="Some guy named jack",
            links=['http://jack-is-myth.blogspot.com'],
            location="Lost forest",
            phone=None
        )
        
        # create the users first
        resp = self.client.post('/user/',
                    data=json.dumps(fixture),
                    headers={'Content-Type':'application/json'}
        )
        self.assertTrue(resp.json['ok'])
        self.assertIsNotNone(resp.json['objects'])
        self.assertEqual(len(resp.json['objects']), 1)
        # get the user's uri
        fixture['uri'] = resp.json['objects'][0]['uri']
        from_date = date(2013, 01, 01)
        to_date = date(2013, 12, 31)
        
        url = '%s/events?from=%s&to=%s' % (fixture['uri'], from_date, to_date)
        resp = self.client.get(url)
        
        self.assert200(resp)
        self.assertTrue(resp.json['ok'])
        self.assertIsNotNone(resp.json['objects'])

    def test_retrieve_users_sheets(self):
        pass
