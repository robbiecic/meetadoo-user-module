#
# dynamo_user.py
#
# This file will create the new table store main user details in dynamodb

from aws.aws import create_dynamodb_resource
from botocore.exceptions import ClientError

# Create dynamodb instance
client = create_dynamodb_resource()

try:
    table = client.create_table(
        TableName='Pending_User',
        KeySchema=[
            {
                'AttributeName': 'email_address',
                'KeyType': 'HASH'  # Partition key, unique
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'email_address',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }

    )
except ClientError as ce:
    print("ERROR CREATING TABLE - ", ce.response)
