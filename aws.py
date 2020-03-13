import boto3
import json

# Read JSON data into the datastore variable
with open('config.json') as json_file:
    data = json.load(json_file)


def create_dynamodb_client():
    return boto3.client('dynamodb', region_name=data['aws']['region_name'], aws_access_key_id=data['aws']['aws_access_key_id'],
                        aws_secret_access_key=data['aws']['aws_secret_access_key'])


def create_dynamodb_resource():
    return boto3.resource('dynamodb', region_name=data['aws']['region_name'], aws_access_key_id=data['aws']['aws_access_key_id'],
                          aws_secret_access_key=data['aws']['aws_secret_access_key'])
