#
# dynamo_user.py
#
# This file will create the new table store main user details in dynamodb

from ... import aws
from botocore.exceptions import ClientError

# Create dynamodb instance
client = aws.create_dynamodb_client()

try:
    table = client.create_table(
        TableName='Movies',
        KeySchema=[
            {
                'AttributeName': 'year',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'year',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
except ClientError as ce:
    print("ERROR CREATING TABLE - ", ce.response)
