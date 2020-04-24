
import json
import bcrypt
import jwt
import base64
from datetime import datetime
from datetime import timedelta
from boto3.dynamodb.conditions import Key, Attr
from aws.aws import create_dynamodb_client, create_dynamodb_resource
from aws.secrets import get_secrets
from EmailService import EmailService


# Create dynamodb instance
dynamodb_client = create_dynamodb_client()
dynamodb_resource = create_dynamodb_resource()
table = dynamodb_resource.Table('User')

# Read JSON data into the datastore variable
data = json.loads(get_secrets())


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
        if bcrypt.checkpw(password + data['hash_secret'].encode('utf-8'), hashed_password):
            expiry_time = datetime.utcnow() + timedelta(seconds=60 * 30)
            encoded_jwt = jwt.encode(
                {'email': email, 'exp': expiry_time}, data['jwt_encode'], algorithm='HS256').decode('utf-8')
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
        payload = jwt.decode(
            encoded_jwt, data['jwt_encode'], algorithms=['HS256'])
    except Exception as identifier:
        return custom_400('JWT INVALID')
    # if valid ensure not expired token
    expiration = datetime.fromtimestamp(payload['exp'])
    current_time = datetime.utcnow()
    if current_time <= expiration:
        return {'statusCode': 200, 'response': str(payload['email'])}
    else:
        return custom_400('Token expired or not valid')


def validate_email(email, jwt):
    response = isAuthenticated(jwt)
    email = response['response']
    if response['statusCode'] == 200:
        response = dynamodb_client.get_item(
            TableName='Pending_User', Key={'email_address': {'S': email}})
        item = {'email_address': response['Item']['email_address'], 'first_name': response['Item']
                ['first_name'], 'surname': response['Item']['surname'], 'password': response['Item']['password']}
        response2 = dynamodb_client.put_item(
            TableName='User', Item=item)
        dynamodb_client.delete_item(TableName='Pending_User', Key={
                                    'email_address': {'S': email}})
        return {'statusCode': 200, 'response': ''}
    else:
        dynamodb_client.delete_item(TableName='Pending_User', Key={
                                    'email_address': {'S': email}})
        return custom_400('Your token has expired, please re-create an account at http://www.meetadoo.com')


def create_user(body):
    # Body must contain the user object
    try:
        email = body['email']
        firstname = body['firstname']
        surname = body['surname']
        hashed_password = encrypt_string(body['password'])
        # Set JWT as 24 hours from now
        expiry_time = datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        encoded_jwt = jwt.encode(
            {'email': email, 'exp': expiry_time}, data['jwt_encode'], algorithm='HS256').decode('utf-8')
        item = {'email_address': {'S': email}, 'first_name': {
            'S': firstname}, 'surname': {'S': surname}, 'password': {'B': hashed_password}, 'jwt': {'S': encoded_jwt}}

        # Check if user exists before creating
        if return_pending_user(email) == 0:
            # Send item to User table
            response = dynamodb_client.put_item(
                TableName='Pending_User', Item=item)
            # Send welcome email
            email_object = EmailService(email, encoded_jwt)
            email_object.send_welcome_email()
            return {'statusCode': 200, 'response': encoded_jwt}
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


def remove_pending_user(email):
    if return_pending_user(email) != 0:
        dynamodb_client.delete_item(TableName='Pending_User', Key={
                                    'email_address': {'S': email}})
        return('Removed User Successfully - ' + str(email))
    else:
        return custom_400('No User found')


def get_user(email_address):
    user = return_user(email_address)
    return_body = {}
    return_body["firstname"] = user['first_name']['S']
    return_body["surname"] = user['surname']['S']
    return_body["email"] = email_address
    if user != 0:
        return {'statusCode': 200, 'response': str(return_body)}
    else:
        return custom_400('No User found')


def get_user_list():
    users_returns = table.scan(
        ProjectionExpression="email_address, first_name, surname")
    my_list = []
    email_only_list = []
    name_only_list = []

    try:
        users_returns['Items']
    except:
        return custom_400('No User found')

    for x in users_returns['Items']:
        my_list.append({"email": x['email_address'],
                        "name": x['first_name'] + ' ' + x['surname'],
                        "avatar": x['first_name'][0] + x['surname'][0]})
        email_only_list.append(x['email_address'])
        name_only_list.append(x['first_name'] + ' ' + x['surname'])

    response_list = {"link_list": my_list,
                     "email_only": email_only_list, "name_only": name_only_list}

    return {'statusCode': 200, 'response': str(response_list)}


def return_user(email_address):
    response = dynamodb_client.get_item(
        TableName='User', Key={'email_address': {'S': email_address}})
    # Check if an user existsx
    try:
        user = response['Item']
        return user
    except:
        return 0


def return_pending_user(email_address):
    response = dynamodb_client.get_item(
        TableName='Pending_User', Key={'email_address': {'S': email_address}})
    # Check if an user existsx
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
               timedelta(seconds=60 * 60 * 24)).strftime("%a, %d %b %Y %H:%MM:%S GMT")
    # Will remove HttpOnly and see if that works
    # Will take out secure for now, doesn't work in dev
    cookie_string = 'jwt=' + \
        str(jwt) + ';  expires=' + \
        str(expires) + \
        "; Path=/; Max-Age=3600; Domain=www.meetadoo.com; HttpOnly; Secure"
    return cookie_string


def set_expired_cookie():
    jwt = "Empty"
    # Set Expiry to 1 day ago
    expires = (datetime.utcnow() -
               timedelta(seconds=60 * 60 * 24)).strftime("%a, %d %b %Y %H:%M:%S GMT")
    cookie_string = 'jwt=' + str(jwt) + ';  expires=' + str(expires) + \
        "; Path=/; Max-Age=3600; Domain=www.meetadoo.com; HttpOnly; Secure"
    return cookie_string


def encrypt_string(string_to_encrypt):
    salt = bcrypt.gensalt()
    combo_password = string_to_encrypt.encode(
        'utf-8') + data['hash_secret'].encode('utf-8')
    hashed_password = bcrypt.hashpw(combo_password, salt)
    return hashed_password
