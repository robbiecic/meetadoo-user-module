
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
                {'email': email, 'exp': expiry_time}, 'NoteItUser', algorithm='HS256')
            return {'statusCode': 200, "token": str(encoded_jwt)}
        else:
            return custom_400('PASSWORD DID NOT MATCH')


def isAuthenticated(body):
    #encoded_jwt = body['jwt']
    encoded_jwt = str(body['jwt'][1:len(body['jwt'])])
    encoded_jwt = encoded_jwt.replace('.', '=')
    decoded_jwt = str(base64.b64decode(encoded_jwt))

    # Get position of expiration datetime
    email_start = str(decoded_jwt).find('email', 0)
    sub_string = decoded_jwt[email_start - 2:255]
    sub_string = sub_string.replace("'", "")
    d = json.loads(sub_string)
    #decoded_email = d['email']
    expiration = datetime.fromtimestamp(d['exp'])
    current_time = datetime.utcnow()
    if current_time <= expiration:
        return {'statusCode': 200}
    else:
        return custom_400('JWT NOT VALID')


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
            return {'statusCode': 200, 'response': str(response)}
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


def encrypt_string(string_to_encrypt):
    salt = bcrypt.gensalt()
    combo_password = string_to_encrypt.encode(
        'utf-8') + master_secret_key.encode('utf-8')
    hashed_password = bcrypt.hashpw(combo_password, salt)
    return hashed_password
