
# cntl-alt-n - to start
# cntl-alt-m - to finish

# Need to install - py-bcrypt, json, flask

import json
from flask import Flask, request, abort, redirect, url_for
import aws
import json
import bcrypt
import jwt
import base64

app = Flask(__name__)

# Create dynamodb instance
dynamodb_client = aws.create_dynamodb_client()

# Set Master key for cryptography
master_secret_key = 'RobboSecretKey123'


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/login', methods=['POST'])
def login():
    # Validate email and password
    # If validated, return JWT
    body = json.loads(request.data)
    email = body['email']
    password = body['password'].encode('utf-8')
    #hashed_password = encrypt_string(body['password'])
    # Check if user exists first
    user_details = return_user(email)
    if user_details == 0:
        return custom_400('ERROR: User not found')
    else:
        hashed_password = user_details['password']['B']
        # Check if password matches
        if bcrypt.checkpw(password+master_secret_key.encode('utf-8'), hashed_password):
            encoded_jwt = jwt.encode(
                {'email': email}, 'NoteItUser', algorithm='HS256')
            return encoded_jwt
        else:
            return custom_400('PASSWORD DID NOT MATCH')


@app.route('/isAuthenticated', methods=['POST'])
def isAuthenticated():
    # Get Parameters
    body = json.loads(request.data)
    encoded_jwt = body['jwt']
    encoded_jwt = base64.b64encode(encoded_jwt)
    print(encoded_jwt)
    decoded_email = jwt.decode(
        str(encoded_jwt), 'NoteItUser', algorithms=['HS256']).decode('utf-8')
    print(decoded_email)
    # If JWT is secure, the email address would be valid
    if return_user(decoded_email) != 0:
        return 'TRUE'
    else:
        return custom_400('JWT NOT VALID')


@app.route('/createUser', methods=['POST'])
def create_user():
    # Body must contain the user object
    try:
        body = json.loads(request.data)
        email = body['email']
        firstname = body['firstname']
        surname = body['surname']

        # for updates, password will not exist
        hashed_password = encrypt_string(body['password'])
        item = {'email_address': {'S': email}, 'first_name': {
            'S': firstname}, 'surname': {'S': surname}, 'password': {'B': hashed_password}}

        # Check if user exists before creating
        if return_user(email) == 0:
            # Send item to User table
            response = dynamodb_client.put_item(TableName='User', Item=item)
            return str(response)
        else:
            return custom_400('ERROR: A user with this email address already exists.')
    except Exception as e:
        print(e)
        return custom_400('User body was poorly formed')


@app.route('/getUser', methods=['GET'])
def get_user():
    try:
        # Argument 1 - email address
        email = str(request.args.get('email'))
        # Get data from dynamoDB
        response = dynamodb_client.get_item(
            TableName='User', Key={'email_address': {'S': email}}, AttributesToGet=['email_address'])
        # Check if an user exists
        try:
            user = response['Item']
            return str(user)
        except:
            return custom_400('ERROR: User not found - ' + str(email))
    except Exception as e:
        print('/getUser' + str(e))
        return custom_400('Email Address not found or badly formed request ' + str(email))


@app.route('/updateUser', methods=['POST'])
def update_user():
    # Can't update key which is email address. Might need a change email address method which removes Item and creates new
    body = json.loads(request.data)
    email = str(body['email'])
    new_firstname = str(body['firstname'])
    new_surname = str(body['surname'])
    try:
        # Remove user record from dynamoDB if exists
        if return_user(email) != 0:
            dynamodb_client.update_item(TableName='User', Key={'email_address': {'S': email}},
                                        UpdateExpression="SET first_name = :firstnameUpdated, surname = :surnameUpdated",
                                        ExpressionAttributeValues={':firstnameUpdated': {'S': new_firstname}, ':surnameUpdated': {'S': new_surname}})
            return 'Updated User - ' + email
        else:
            return custom_400('No User found')
    except Exception as E:
        return custom_400(str(E))


@app.route('/removeUser', methods=['POST'])
def remove_user():
    body = json.loads(request.data)
    email = body['email']
    if return_user(email) != 0:
        dynamodb_client.delete_item(TableName='User', Key={
                                    'email_address': {'S': email}})
        return('Removed User Successfully - ' + str(email))
    else:
        return custom_400('No User found')


def return_user(email_address):
    response = dynamodb_client.get_item(
        TableName='User', Key={'email_address': {'S': email_address}})
    # Check if an user exists
    try:
        user = response['Item']
        return user
    except:
        return 0


def custom_400(message):
    abort(400, description=message)


def encrypt_string(string_to_encrypt):
    salt = bcrypt.gensalt()
    combo_password = string_to_encrypt.encode(
        'utf-8') + master_secret_key.encode('utf-8')
    hashed_password = bcrypt.hashpw(combo_password, salt)
    return hashed_password


def compare_passwords(existing_password, new_password):
    #existing_password =- bcrypt.hashpw('existing_password', existing_password)
    if (existing_password == new_password):
        return 1
    else:
        return 0


if __name__ == '__main__':
    app.run()
