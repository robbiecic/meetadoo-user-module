import boto3
from botocore.exceptions import ClientError
from aws.aws import create_ses_client
import json
from aws.secrets import get_secrets


class EmailService:

    def __init__(self, recipient_email: str, additional_content: str):
        self.recipient_email = recipient_email
        self.settings = json.loads(get_secrets())
        self.additional_content = str(additional_content)

    def __del__(self):
        self.settings = None
        self.recipient_email = None

    def send_welcome_email(self):
        base_url = 'https://www.meetadoo.com/api/?action=ConfirmEmail'
        url = base_url + '&email=' + self.recipient_email + \
            '&token=' + self.additional_content
        body_html = """<html>
        <head></head>
        <body>
          <h1>Welcome to Meetadoo! </h1>
          <p>Before you can start using it, you must first confirm your account by clicking the link below :) </p>
            <a href='""" + url + """'>Click to confirm your email!</a>
          <p>If you feel that you didn't register and fraud is suspected, please email us on info@meetadoo.com </p>
        </body>
        </html>
                    """
        body_text = ("""Welcome to Meetadoo! \r\n"
                     "Before you can start using it, you must first confirm your account by clicking the link below :) \r\n"""
                     + url + """\r\n"
                     "If you feel that you didn't register and fraud is suspected, please email us on info@meetadoo.com
                     """
                     )

        self.send_email('Welcome to Meetadoo!',
                        body_text, body_html)

    def send_email(self, subject, body_text, body_html):
        # Only send email if configuration is set to true
        if self.settings['email_enabled'] == 'True':
            # Send email is stored in AWS secret manager
            SENDER = self.settings['email_sender_address']

            # The character encoding for the email.
            CHARSET = "UTF-8"

            # Create a new SES resource and specify a region.
            client = create_ses_client()

            # Try to send the email.
            try:
                # Provide the contents of the email.
                response = client.send_email(
                    Destination={
                        'ToAddresses': [
                            self.recipient_email,
                        ],
                    },
                    Message={
                        'Body': {
                            'Html': {
                                'Charset': CHARSET,
                                'Data': body_html,
                            },
                            'Text': {
                                'Charset': CHARSET,
                                'Data': body_text,
                            },
                        },
                        'Subject': {
                            'Charset': CHARSET,
                            'Data': subject,
                        },
                    },
                    Source=SENDER
                    # If you are not using a configuration set, comment or delete the
                    # following line
                    # ConfigurationSetName=CONFIGURATION_SET,
                )
            # Display an error if something goes wrong.
            except ClientError as e:
                print(e.response['Error']['Message'])
            else:
                print("Email sent! Message ID:"),
                print(response['MessageId'])
        else:
            print("Email not sent - email service is disabled.")
