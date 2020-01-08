
# cntl-alt-n - to start
# cntl-alt-m - to finish

import decimal
import json
from flask import Flask, request, abort
import aws

app = Flask(__name__)

# Create dynamodb instance
dynamodb_client = aws.create_dynamodb_client()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/createUser')
def create_user():
    # Argument 1 - email
    email = request.args.get('email')
    # Argument 2 - firstname
    firstname = request.args.get('firstname')
    # Send item to User table
    response = dynamodb_client.put_item(TableName='User', Item={
        'email_address': {'S': email}, 'first_name': {'S': firstname}})

    return response


@app.route('/getUser')
def get_user():
    try:
        # Argument 1 - email address
        email = request.args.get('email')
        # Get data from dynamoDB
        response = dynamodb_client.get_item(
            TableName='User', Key={'email_address': {'S': email}})
        return response
    except:
        return custom_400('Email Address not provided or badly formed request.')


def custom_400(message):
    abort(400, description=message)


if __name__ == '__main__':
    app.run()
