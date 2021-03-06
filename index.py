import json
from api_handler import API_Handler


def lambda_handler(event, context):
    # This API is driven off the query string parameter 'action'
    # Set parameters to pass into class
    try:
        body = json.loads(event['body'])
    except:
        body = {}

    print('event - ', event)
    # Create Class and process event
    API = API_Handler(event['queryStringParameters'],
                      event['httpMethod'], body, event['headers'])
    return API.run_action()
