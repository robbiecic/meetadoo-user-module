
# cntl-alt-n - to start
# cntl-alt-m - to finish

# Need to install - py-bcrypt, json, flask

import json
from flask import Flask, request, abort, redirect, url_for
import aws
import json
import bcrypt
import jwt

app = Flask(__name__)

# Create dynamodb instance
dynamodb_client = aws.create_dynamodb_client()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/login', methods=['POST'])
def login():
    # Validate email and password
    # If validated, return JWT
    body = json.loads(request.data)
    email = body['email']
    hashed_password = encrypt_string(body['password'])
    # Check if user exists first
    user_details = return_user(email)
    if user_details == 0:
        return 'ERROR: User not found'
    else:
        # Check if password matches
        if compare_passwords(user_details['password'], hashed_password):
            encoded_jwt = jwt.encode(
                {'email': email}, 'NoteItUser', algorithm='HS256')
            return encoded_jwt
        else:
            return 'PASSWORD DID NOT MATCH'


@app.route('/isAuthenticated', methods=['GET'])
def isAuthenticated():
    # Get Parameters
    encoded_jwt = request.args.get('jwt')
    decoded_email = jwt.decode(encoded_jwt, 'NoteItUser', algorithms=['HS256'])
    # If JWT is secure, the email address would be valid
    if return_user(decoded_email) != 0:
        return 'TRUE'
    else:
        return 'FALSE'


@app.route('/createUser', methods=['POST'])
def create_user():
    # Body must contain the user object
    try:
        body = json.loads(request.data)
        email = body['email']
        firstname = body['firstname']
        surname = body['surname']
        hashed_password = encrypt_string(body['password'])
        # Check if user exists before creating
        if return_user(email) == 0:
            # Send item to User table
            response = dynamodb_client.put_item(TableName='User', Item={
                'email_address': {'S': email}, 'first_name': {'S': firstname}, 'surname': {'S': surname}, 'password': {'B': hashed_password}})
            return response
        else:
            return custom_400('ERROR: A user with this email address already exists.')
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
            return str(user)
        except:
            return 'ERROR: User not found - ' + str(email)
    except:
        return custom_400('Email Address not provided or badly formed request'+str(email))


@app.route('/updateUser', methods=['POST'])
def update_user():
    # In dynamodb is easier to drop and create a user record
    body = json.loads(request.data)
    email = body['email']
    # !!!! NEED TO CHECK IF BODY IS VALID BEFORE WE COMMIT TO DELETING OTHERWISE WE CAN'T RECREATE

    # Remove user record from dynamoDB if exists
    if return_user(email) != 0:
        dynamodb_client.delete_item(TableName='User', Key={
                                    'email_address': {'S': email}})
        # Redirect to create the user again. code 307 represents a post, body of request will retain during redirect
        return redirect(url_for('create_user'), code=307)
    else:
        return custom_400('No User found')


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
    master_secret_key = 'RobboSecretKey123'
    salt = bcrypt.gensalt()
    combo_password = string_to_encrypt.encode('utf-8') + \
        salt + master_secret_key.encode('utf-8')
    hashed_password = bcrypt.hashpw(combo_password, salt)
    return hashed_password


def compare_passwords(existing_password, new_password):
    new_hash = encrypt_string(new_password)
    is_same_password = bcrypt.hashpw(new_hash, existing_password)
    return is_same_password


if __name__ == '__main__':
    app.run()
