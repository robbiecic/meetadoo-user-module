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

    # Test basic HTML response from parent URL
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # Create test user
    # def test_valid_user_registration(self):
    #     response = self.app.post(
    #         '/createUser',
    #         data=json.dumps(dict(email='test@NoteIt.com',
    #                              password='TestPassword123', firstname='Test', surname='TestSurnace')), content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, 200)

    # Get Test User
    def test_get_user(self):
        email_query = '{"email": "test@NoteIt.com"}'
        a = json.dumps(email_query)
        a = a.replace("\\", "")
        print(a)
        with app.test_request_context():
            response = self.app.get(url_for('get_user'),
                                    query_string=a)
            print(response)
            print(response.data)
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
