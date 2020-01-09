
# cntl-alt-n - to start
# cntl-alt-m - to finish

import decimal
import json
from flask import Flask, request, abort, redirect, url_for
import aws
import json

app = Flask(__name__)

# Create dynamodb instance
dynamodb_client = aws.create_dynamodb_client()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/createUser', methods=['POST'])
def create_user():
    # Body must contain the user object
    try:
        body = json.loads(request.data)
        email = body['email']
        firstname = body['firstname']
        surname = body['surname']
        # Send item to User table
        response = dynamodb_client.put_item(TableName='User', Item={
            'email_address': {'S': email}, 'first_name': {'S': firstname}, 'surname': {'S': surname}})
        return response
    except Exception as e:
        print(e)
        return custom_400('User body was poorly formed')


@app.route('/getUser', methods=['GET'])
def get_user():
    try:
        # Argument 1 - email address
        email = request.args.get('email')
        # Get data from dynamoDB
        response = dynamodb_client.get_item(
            TableName='User', Key={'email_address': {'S': email}})
        # Check if an user exists
        try:
            user = response['Item']
            return user
        except:
            return 'ERROR: User not found'
    except:
        return custom_400('Email Address not provided or badly formed request.')


@app.route('/updateUser', methods=['POST'])
def update_user():
    # In dynamodb is easier to drop and create a user record
    body = json.loads(request.data)
    email = body['email']
    # Remove user record from dynamoDB if exists
    if does_user_exist(email) == 1:
        dynamodb_client.delete_item(TableName='User', Key={
                                    'email_address': {'S': email}})
        # Redirect to create the user again. code 307 represents a post, body of request will retain during redirect
        return redirect(url_for('create_user'), code=307)
    else:
        return custom_400('No User found')


def does_user_exist(email_address):
    response = dynamodb_client.get_item(
        TableName='User', Key={'email_address': {'S': email_address}})
    # Check if an user exists
    try:
        a = response['Item']
        return 1
    except:
        return 0


def custom_400(message):
    abort(400, description=message)


if __name__ == '__main__':
    app.run()
