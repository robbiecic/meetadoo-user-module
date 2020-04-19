import unittest
from my_email import EmailService
import warnings

# Data set up only for this unit test. WIll be teared down after
recipient = 'robert.cicero.rc@gmail.com'


class emailTestCase(unittest.TestCase):

    # Remove Test User
    @classmethod
    def tearDownClass(cls):
        pass

    @classmethod
    def setUp(self):
        warnings.filterwarnings(
            "ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")

    # Create test user
    def test_send_email(self):
        body_text = 'This email was generated as part of a Unit Test. Please ignore or Delete this email.'
        body_html = '<h1>This email was generated as part of a Unit Test. Please ignore or Delete this email. </h1>'
        email_object = EmailService(recipient)
        response = email_object.send_email(
            'Unit Test Email', body_text, body_html)
        del email_object
        # self.assertEqual(response['statusCode'], 200)

    def test_send_welcome_email(self):
        email_object = EmailService(recipient)
        response = email_object.send_welcome_email()
        del email_object

# End of emailTestCase --------------------------------------------------------------------------------------------------------------------


def suite():  # Need to define a suite as setUp and tearDown are called per test otherwise
    suite = unittest.TestSuite()
    suite.addTest(emailTestCase('test_send_email'))
    suite.addTest(emailTestCase('test_send_welcome_email'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
