import unittest
import json
import requests

# Import test data
with open('tests/create_user.json') as json_file:
    json_data = json.load(json_file)
with open('tests/remove_user.json') as json_file:
    json_data_remove = json.load(json_file)

# Set URL where API calls are made
url = "https://i6vtmh1eq3.execute-api.ap-southeast-2.amazonaws.com/Development"


class E2ETestCase(unittest.TestCase):

    # Remove Test User
    @classmethod
    def tearDownClass(cls):
        requests.post(url=url, data=json.dumps(json_data_remove), headers={
            'content-type': 'application/json'})

    # Create test user
    def test_valid_user_registration(self):
        # sending get request and saving the response as response object
        response = requests.post(url=url, data=json.dumps(json_data), headers={
                                 'content-type': 'application/json'})
        print(response.content)
        self.assertEqual(response.status_code, 200)

# End of E2ETestCase --------------------------------------------------------------------------------------------------------------------


def suite():  # Need to define a suite as setUp and tearDown are called per test otherwise
    suite = unittest.TestSuite()
    suite.addTest(E2ETestCase('test_valid_user_registration'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
