import json
from post import create_user, remove_user, login


def lambda_handler(event, context):
    # This API is driven off the query string parameter 'request_action'
    try:
        # For every request, we require a data object containing at least the email
        try:
            bodydata = json.loads(event['body'])
        except:
            bodydata = event['body']

        action = event['queryStringParameters']['action']
        body = bodydata['data']
        email = body['email']
    except Exception as identifier:
        return {
            'statusCode': 400,
            'body': 'Body Not formed properly' + str(identifier)
        }

    # Enter if statement block to route message
    if (action == 'CreateUser'):
        result = create_user(body)
        return {
            "headers": {"Set-Cookie": result['cookie']},
            'statusCode': result['statusCode'],
            'body': result['response']
        }
    elif (action == 'RemoveUser'):
        result = remove_user(email)
        return {
            'statusCode': result['statusCode'],
            'body': result['response']
        }
    elif (action == 'Login'):
        result = login(body)
        return {
            "headers": {"Set-Cookie": result['cookie']},
            'statusCode': result['statusCode'],
            'body': result['response']
        }
    elif (action == 'isAuthenticated'):
        result = isAuthenticated(body)
        return {
            'statusCode': result['statusCode'],
            'body': result['response']
        }
    elif (action == 'UpdateUser'):
        result = update_user(body)
        return {
            'statusCode': result['statusCode'],
            'body': result['response']
        }
    else:
        return {
            'statusCode': 400,
            'body': "A valid request action was not provided"
        }
