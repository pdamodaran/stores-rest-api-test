from models.user import UserModel
from tests.test_base import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            # need to save to database
            with self.app_context():
                response = client.post('/register', data={'username': 'test', 'password': 1234})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message' : 'User created successfully.'}, json.loads(response.data))



    def test_register_and_login(self):
        with self.app() as client:
            # need to save to database
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                auth_response = client.post('/auth', data=json.dumps({
                    'username': 'test',
                    'password': '1234'
                }), headers={'Content-Type': 'application/json'})

                #checks to see if the access token is included in the keys of the response data
                self.assertIn('access_token', json.loads(auth_response.data).keys())


    def test_user_already_exists(self):
        with self.app() as client:
            # need to save to database
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': 1234})
                response = client.post('/register', data={'username': 'test', 'password': 1234})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message' : 'A user already exists with that username.'}, json.loads(response.data))


