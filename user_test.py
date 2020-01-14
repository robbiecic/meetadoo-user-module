import unittest
import user
from user import app
import json
from flask import url_for


class UserTestCase(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

    # Remove Test User
    def tearDown(self):
        self.app.post(
            '/removeUser',
            data=json.dumps(dict(email='test@NoteIt.com')),
            content_type='application/json')

    # Test basic HTML response from parent URL
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # Create test user
    def test_valid_user_registration(self):
        response = self.app.post(
            '/createUser',
            data=json.dumps(dict(email='test@NoteIt.com',
                                 password='TestPassword123', firstname='Test', surname='TestSurnace')), content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    # Get Test User
    def test_get_user(self):
        response = self.app.get(
            '/getUser', query_string='email=test@NoteIt.com', content_type='application/json')
        email_start = str(response.data).find('email_address', 0)
        print(response.data)
        self.assertEqual(response.status_code, 200)
        # If email address is found in the return string, then it successfully finds the email
        self.assertGreater(email_start, 0)


if __name__ == '__main__':
    unittest.main()
