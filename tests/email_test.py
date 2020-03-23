import unittest
from my_email import send_email

# Data set up only for this unit test. WIll be teared down after
recipient = 'robert.cicero.rc@gmail.com'


class emailTestCase(unittest.TestCase):

    # Remove Test User
    @classmethod
    def tearDownClass(cls):
        pass

    # Create test user
    def test_send_email(self):
        response = send_email(recipient, 'Unit Test Email',
                              'This email was generated as part of a Unit Test. Please ignore or Delete this email.')
        # self.assertEqual(response['statusCode'], 200)


# End of UserTestCase --------------------------------------------------------------------------------------------------------------------


def suite():  # Need to define a suite as setUp and tearDown are called per test otherwise
    suite = unittest.TestSuite()
    suite.addTest(emailTestCase('test_send_email'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
