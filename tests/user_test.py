import unittest
from post import login, create_user, remove_user

user_object = {"email": "test@NoteIt.com",
               "password": "TestPassword123", "firstname": "Test", "surname": "Test Surname"}


class UserTestCase(unittest.TestCase):

    # # executed prior to each test
    # @classmethod
    # def setUpClass(cls):
    #     app.config['TESTING'] = True
    #     app.config['WTF_CSRF_ENABLED'] = False
    #     app.config['DEBUG'] = False
    #     cls.app = app.test_client()

    # Remove Test User
    @classmethod
    def tearDownClass(cls):
        remove_user('test@NoteIt2.com')
        remove_user('test@NoteIt2.com')

    # Create test user
    def test_create_user(self):
        response = create_user(user_object)
        self.assertEqual(response['statusCode'], 200)

    # # Get Test User
    # def test_get_user(self):
    #     response = self.app.get(
    #         '/getUser', query_string='email=test@NoteIt.com', content_type='application/json')
    #     email_start = str(response.data).find('email_address', 0)
    #     self.assertEqual(response.status_code, 200)
    #     # If email address key is found in the return string, then it successfully finds the email
    #     self.assertGreater(email_start, 0)

    # # Update Test User
    # def test_update_user(self):
    #     response = self.app.post(
    #         '/updateUser',
    #         data=json.dumps(dict(email='test@NoteIt.com', firstname='Test', surname='Test Surname')), content_type='application/json', follow_redirects=True
    #     )
    #     # Need to handle redirect in above call
    #     self.assertEqual(response.status_code, 200)

    # # Test Login
    # def test_login(self):
    #     response = self.app.post(
    #         '/login',
    #         data=json.dumps(dict(email='test@NoteIt.com',
    #                              password='TestPassword123')), content_type='application/json')
    #     # Need to handle redirect in above call
    #     self.assertEqual(response.status_code, 200)
    #     # Store returned JWT so we can test the isAuthenticated method
    #     jwt_response = json.loads(response.data)
    #     jwt_response = jwt_response['token']
    #     response = self.app.post(
    #         '/checkJWT', data=json.dumps(dict(jwt=str(jwt_response))), content_type='application/json')
    #     self.assertEqual(response.status_code, 200)

    # # Test Failed Login

    # def test_failed_login(self):
    #     response = self.app.post(
    #         '/login',
    #         data=json.dumps(dict(email='test@NoteIt.com',
    #                              password='WRONGPASSWORD')), content_type='application/json')
    #     # Need to handle redirect in above call
    #     self.assertEqual(response.status_code, 400)

# End of UserTestCase --------------------------------------------------------------------------------------------------------------------


def suite():  # Need to define a suite as setUp and tearDown are called per test otherwise
    suite = unittest.TestSuite()
    suite.addTest(UserTestCase('test_create_user'))
    # suite.addTest(UserTestCase('test_valid_user_registration'))
    # suite.addTest(UserTestCase('test_get_user'))
    # suite.addTest(UserTestCase('test_update_user'))
    # suite.addTest(UserTestCase('test_login'))
    # suite.addTest(UserTestCase('test_failed_login'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
