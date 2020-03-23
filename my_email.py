import boto3
from botocore.exceptions import ClientError
import aws
import json


def send_email(recipient, subject, body_text):

    # Read JSON data into the datastore variable
    with open('config.json') as json_file:
        data = json.load(json_file)

    if data['email_settings']['enabled'] == True:

        SENDER = data['email_settings']['sender_email']

        # CONFIGURATION_SET = "ConfigSet"

        # The email body for recipients with non-HTML email clients.
        # BODY_TEXT = ("Amazon SES Test (Python)\r\n"
        #              "This email was sent with Amazon SES using the "
        #              "AWS SDK for Python (Boto)."
        #              )

        # The HTML body of the email.
        BODY_HTML = """<html>
        <head></head>
        <body>
          <h1>Amazon SES Test (SDK for Python)</h1>
          <p>This email was sent with
            <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
            <a href='https://aws.amazon.com/sdk-for-python/'>
              AWS SDK for Python (Boto)</a>.</p>
        </body>
        </html>
                    """

        # The character encoding for the email.
        CHARSET = "UTF-8"

        # Create a new SES resource and specify a region.
        client = aws.create_ses_client()

        # Try to send the email.
        try:
            # Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        recipient,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML,
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
