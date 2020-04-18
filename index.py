import json
from user_functions import create_user, remove_user, login, get_user, isAuthenticated, update_user, get_user_list, set_expired_cookie
from api_handler import API_Handler


def lambda_handler(event, context):
    # This API is driven off the query string parameter 'request_action'
    # print('Event details- ', str(event))
    # Set parameters to pass into class
    print('Context - ', context)
    print('Event - ', event)
    header = {}
    try:
        body = json.loads(event['body'])
    except:
        body = {}

    # Create Class and process event
    API = API_Handler(event['queryStringParameters']['action'],
                      event['httpMethod'], body, event['headers'])
    return API.run_action()
