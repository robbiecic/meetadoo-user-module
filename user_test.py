import unittest
import user
from user import app
import json


class UserTestCase(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

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

    # Remove test user


if __name__ == '__main__':
    unittest.main()
