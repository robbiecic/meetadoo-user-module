import json
from post import create_user, remove_user


def lambda_handler(event, context):

    # This API is driven off the body containing the attribute 'request_action'
    try:
        bodydata = json.loads(event['body'])
        action = event["queryStringParameters"]['action']
        body = bodydata['data']
        email = body['email']

        if (action == 'CreateUser'):
            result = create_user(body)
            return {
                'statusCode': result['statusCode'],
                'body': result['response']
            }
        elif (action == 'RemoveUser'):
            result = remove_user(email)
            return {
                'statusCode': result['statusCode'],
                'body': result['response']
            }
        else:
            return {
                'statusCode': 400,
                'body': "A valid user action was not provided"
            }
    except Exception as identifier:
        return {
            'statusCode': 400,
            'body': 'Body Not formed properly' + str(identifier)
        }
