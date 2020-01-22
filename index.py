import json
from post import create_user


def lambda_handler(event, context):

    # This API is driven off the body containing the attribute 'request_action'
    try:
        bodydata = json.loads(event['body'])
        action = bodydata['request_action']
        body = bodydata['data']

        return {
            'statusCode': 200,
            'body': 'Status OK'
        }
    except Exception as identifier:
        return {
            'statusCode': 400,
            'body': 'Body Not formed properly' + str(identifier)
        }

    # if (action == 'Create User'):
    #     result = create_user(body)
    #     return {
    #         'statusCode': result['statusCode'],
    #         'body': result['response']
    #     }
