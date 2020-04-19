import unittest
from user_functions import login, create_user, remove_user, update_user, isAuthenticated, return_user, get_user, get_user_list, remove_pending_user, validate_email
from index import lambda_handler
import json
import warnings

# Data set up only for this unit test. WIll be teared down after
my_email = 'robert.cicero.rc@gmail.com'
user_object = {"email": my_email,
               "password": "TestPassword123", "firstname": "Test", "surname": "Test Surname"}

user_object2 = {"email": my_email,
                "firstname": "New Name", "surname": "New Surname"}

user_object_bad = {"email": my_email,
                   "password": "BAD PASSSWORD", "firstname": "Test", "surname": "Test Surname"}

bad_jwt = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RATm90ZUl0LmNvbSIsImlhdCI6MTUxNjIzOTAyMn0.paCMHeNjrWR5N4t6_eWsZWxTfscugu2gIyacT8zVFyY'


with open('tests/event_login.json') as json_file:
    event_login = json.load(json_file)
with open('tests/event_auth.json') as json_file:
    event_auth = json.load(json_file)


class UserTestCase(unittest.TestCase):

    # Remove Test User
    @classmethod
    def tearDownClass(cls):
        remove_user(my_email)
        remove_pending_user(my_email)

    # Disable warnings, known AWS issue
    @classmethod
    def setUp(self):
        warnings.filterwarnings(
            "ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")

    # Create test user
    def test_create_user(self):
        response = create_user(user_object)
        jwt = response['response']
        self.assertEqual(response['statusCode'], 200)
        response = validate_email(my_email, jwt)
        self.assertEqual(response['statusCode'], 200)

    # # Get Test User
    def test_return_user(self):
        response = return_user(user_object['email'])
        email_start = str(response).find('email_address', 0)
        # If email address key is found in the return string, then it successfully finds the email
        self.assertGreater(email_start, 0)

    # Update Test User
    def test_update_user(self):
        response = update_user(user_object2)
        # Need to handle redirect in above call
        self.assertEqual(response['statusCode'], 200)

    # Test Login
    def test_login(self):
        response = login(user_object)
        self.assertEqual(response['statusCode'], 200)

    # Test Failed Login
    def test_failed_login(self):
        response = login(user_object_bad)
        # Need to handle redirect in above call
        self.assertEqual(response['statusCode'], 400)

    # Test login from lambda function
    def test_lambda_login(self):
        response = lambda_handler(event_login, "")
        self.assertEqual(response['statusCode'], 200)

    # Test get User from Lambda function
    def test_lambda_getAuth(self):
        response = lambda_handler(event_auth, "")
        self.assertEqual(response['statusCode'], 400)

    def test_get_user(self):
        response = get_user(user_object['email'])
        self.assertEqual(response['statusCode'], 200)
        response_data = json.loads(response['response'].replace("'", '"'))
        self.assertEqual(response_data['email'], user_object['email'])

    def test_get_user_list(self):
        response = get_user_list()
        self.assertEqual(response['statusCode'], 200)

# End of UserTestCase --------------------------------------------------------------------------------------------------------------------


def suite():  # Need to define a suite as setUp and tearDown are called per test otherwise
    suite = unittest.TestSuite()
    suite.addTest(UserTestCase('test_create_user'))
    suite.addTest(UserTestCase('test_return_user'))
    suite.addTest(UserTestCase('test_update_user'))
    suite.addTest(UserTestCase('test_login'))
    suite.addTest(UserTestCase('test_failed_login'))
    suite.addTest(UserTestCase('test_lambda_login'))
    suite.addTest(UserTestCase('test_lambda_getAuth'))
    suite.addTest(UserTestCase('test_get_user'))
    suite.addTest(UserTestCase('test_get_user_list'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
