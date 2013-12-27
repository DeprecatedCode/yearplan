# -*- coding utf-8 -*-
from flask.ext.testing import TestCase
import unittest
import json

class AppTest(TestCase):
   
    app_headers = {'Content-type' : 'application/json'}

    def create_app(self):
        from runserver import application
        application.config['MONGODB_DB'] = 'yearplan'
        db = application.extensions['mongoengine']
        db.connection.drop_database(db.app.config.get('MONGODB_DB'))
        return application

    def assert201( self, response ):
        self.assertStatus( response, 201 )

    def assert400( self, response ):
        self.assertStatus(response, 400)
      
    def authenticateUser(self, user):
        auth_response = self.client.post('/auth/',
                        data = json.dumps(user),
                        headers = {'Content-type' : 'application/json'}
        )
      
        self.assert200( auth_response )
        self.assertTrue(auth_response.json['ok'])
        self.assertIsNotNone(auth_response.headers.get('X-yearplan-user', None))
        
        user['api_token'] = auth_response.headers.get('X-yearplan-user')
        return user['api_token']