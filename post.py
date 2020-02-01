
import json
import aws
import json
import bcrypt
import jwt
import base64
from datetime import datetime
from datetime import timedelta


# Create dynamodb instance
dynamodb_client = aws.create_dynamodb_client()

# Set Master key for cryptography
master_secret_key = 'RobboSecretKey123'


def login(body):
    # Validate email and password. If validated, return JWT
    email = body['email']
    password = body['password'].encode('utf-8')
    # Check if user exists first
    user_details = return_user(email)
    if user_details == 0:
        return custom_400('ERROR: User not found')
    else:
        hashed_password = user_details['password']['B']
        # Check if password matches
        if bcrypt.checkpw(password + master_secret_key.encode('utf-8'), hashed_password):
            expiry_time = datetime.utcnow() + timedelta(seconds=60 * 30)
            encoded_jwt = jwt.encode(
                {'email': email, 'exp': expiry_time}, 'NoteItUser', algorithm='HS256').decode('utf-8')
            return_body = {}
            return_body["firstname"] = user_details['first_name']['S']
            return_body["surname"] = user_details['surname']['S']
            return_body["email"] = email
            cookie_string = set_cookie(encoded_jwt)
            return {'cookie': cookie_string, 'statusCode': 200, 'response': str(return_body)}
        else:
            return custom_400('PASSWORD DID NOT MATCH')


def isAuthenticated(encoded_jwt):
    # jwt decode will throw an exception if fails verification
    try:
        payload = jwt.decode(encoded_jwt, 'NoteItUser', algorithms=['HS256'])
    except Exception as identifier:
        return custom_400('JWT INVALID')
    # if valid ensure not expired token
    expiration = datetime.fromtimestamp(payload['exp'])
    current_time = datetime.utcnow()
    if current_time <= expiration:
        return {'statusCode': 200}
    else:
        return custom_400('JWT EXPIRED')


def create_user(body):
    # Body must contain the user object
    try:
        email = body['email']
        firstname = body['firstname']
        surname = body['surname']
        # For updates, password will not exist
        hashed_password = encrypt_string(body['password'])
        item = {'email_address': {'S': email}, 'first_name': {
            'S': firstname}, 'surname': {'S': surname}, 'password': {'B': hashed_password}}

        # Check if user exists before creating
        if return_user(email) == 0:
            # Send item to User table
            response = dynamodb_client.put_item(TableName='User', Item=item)
            expiry_time = datetime.utcnow() + timedelta(seconds=60 * 30)
            encoded_jwt = jwt.encode(
                {'email': email, 'exp': expiry_time}, 'NoteItUser', algorithm='HS256').decode('utf-8')
            return_body = {}
            return_body["firstname"] = firstname
            return_body["surname"] = surname
            return_body["email"] = email
            cookie_string = set_cookie(encoded_jwt)
            return {'cookie': cookie_string, 'statusCode': 200, 'response': str(return_body)}
        else:
            return custom_400('ERROR: A user with this email address already exists.')
    except Exception as e:
        print(e)
        return custom_400('User body was poorly formed')


def update_user(body):
    # Can't update key which is email address. Might need a change email address method which removes Item and creates new
    email = str(body['email'])
    new_firstname = str(body['firstname'])
    new_surname = str(body['surname'])
    try:
        # Remove user record from dynamoDB if exists
        if return_user(email) != 0:
            dynamodb_client.update_item(TableName='User', Key={'email_address': {'S': email}},
                                        UpdateExpression="SET first_name = :firstnameUpdated, surname = :surnameUpdated",
                                        ExpressionAttributeValues={':firstnameUpdated': {'S': new_firstname}, ':surnameUpdated': {'S': new_surname}})
            return {'statusCode': 200, 'response': str('Updated User - ' + email)}
        else:
            return custom_400('No User found')
    except Exception as E:
        return custom_400(str(E))


def remove_user(email):
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
    return {'statusCode': 400, 'response': message}


def set_cookie(jwt):
    # Delete the cookie after 1 day
    expires = (datetime.utcnow() +
               timedelta(seconds=60 * 60 * 24)).strftime("%a, %d %b %Y %H:%M:%S GMT")
    cookie_string = 'jwt=' + \
        str(jwt) + ';  expires=' + \
        str(expires) + "; Secure; HttpOnly"
    return cookie_string


def encrypt_string(string_to_encrypt):
    salt = bcrypt.gensalt()
    combo_password = string_to_encrypt.encode(
        'utf-8') + master_secret_key.encode('utf-8')
    hashed_password = bcrypt.hashpw(combo_password, salt)
    return hashed_password
