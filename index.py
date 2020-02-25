import json
from user_functions import create_user, remove_user, login, get_user, isAuthenticated, update_user, get_user_list, set_expired_cookie


def lambda_handler(event, context):
    # This API is driven off the query string parameter 'request_action'
    print('Event details- ', str(event))

    # This will always be hear as defined by API Gateway rule
    action = event['queryStringParameters']['action']

    # # Check origin - add header if valid origin
    # if event['httpMethod'] == 'POST':
    #     origin = event['headers']['origin']
    # else:
    #     origin = event['headers']['referer']
    # header = {}
    # if origin == "https://dh8knvr6m97wx.cloudfront.net":
    #     header["Access-Control-Allow-Origin"] = "https://dh8knvr6m97wx.cloudfront.net"
    # elif origin == "https://localhost:8080":
    #     header["Access-Control-Allow-Origin"] = "https://localhost:8080"
    # elif origin == "http://localhost:8080":
    #     header["Access-Control-Allow-Origin"] = "http://localhost:8080"
    # else:
    #     header["Access-Control-Allow-Origin"] = "https://dh8knvr6m97wx.cloudfront.net"
    header = {}
    # header["Access-Control-Allow-Credentials"] = "true"

    # If POST then get body
    if event['httpMethod'] == 'POST':
        # Try setting event body, fail if doesn't exist
        try:
            # For every request, we require a data object containing at least the email
            try:
                bodydata = json.loads(event['body'])
            except:
                bodydata = event['body']
        except Exception as identifier:
            return {
                'statusCode': 400,
                'body': 'Body Not formed properly' + str(identifier)
            }
        # Set body data
        body = bodydata['data']
        email = body['email']

    # Locate cookie details if there, if not ignore
    jwt_token = "Something Invalid"
    try:
        # 'cookie' is case sensistive. Is lower case from browser, upper care from Postman
        try:
            cookie = event['headers']['cookie']
        except:
            cookie = event['headers']['cookie']
        print('Cookie - ' + str(cookie))
        # Had to add this as running through AWS, different cookies are added. We want the one starting with jwt
        split_cookie = str(cookie).split(';')
        for x in split_cookie:
            try:
                index = str(x).index("jwt")
                jwt_token = x.replace("jwt", "").replace(
                    " ", "").replace("=", "")
            except:
                # Ignore, index will throw an error meaning the "jwt" doesn't exist
                pass
    except:
        jwt_token = "Something Invalid"

    print('jwt_token - ' + str(jwt_token))

    # Enter if statement block to route message
    if (action == 'CreateUser'):
        result = create_user(body)
        header["Set-Cookie"] = result['cookie']
        return {
            "headers": header,
            'statusCode': result['statusCode'],
            'body': result['response']
        }
    elif (action == 'RemoveUser'):
        result = remove_user(email)
        return {
            'statusCode': result['statusCode'],
            'body': result['response']
        }
    elif (action == 'Login' and event['httpMethod'] == 'POST'):
        result = login(body)
        header["Set-Cookie"] = result['cookie']
        return {
            "headers": header,
            'statusCode': result['statusCode'],
            'body': result['response']
        }
    elif (action == 'Logout' and event['httpMethod'] == 'POST'):
        expired_cookie = set_expired_cookie()
        header["Set-Cookie"] = expired_cookie
        return {
            "headers": header,
            'statusCode': "200",
            'body': "You are now logged out"
        }
    elif (action == 'isAuthenticated'):
        result = isAuthenticated(jwt_token)
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
    elif (action == 'getUser'):
        authenticated_response = isAuthenticated(jwt_token)
        if authenticated_response['statusCode'] == 200:
            print('User pass authentication with response ' +
                  str(authenticated_response))
            # Get email from decoded response. Don't want to store it on client side, but it's in the token which is issued upon successful login
            body_email = authenticated_response['response']
            result = get_user(body_email)
            return {
                'headers': header,
                'statusCode': result['statusCode'],
                'body': result['response']
            }
        else:
            return authenticated_response
    elif (action == 'getUserList'):
        authenticated_response = isAuthenticated(jwt_token)
        if authenticated_response['statusCode'] == 200:
            print('User pass authentication with response ' +
                  str(authenticated_response))
            result = get_user_list()
            return {
                'statusCode': result['statusCode'],
                'body': result['response']
            }
        else:
            return authenticated_response
    else:
        return {
            'statusCode': 400,
            'body': "A valid request action was not provided"
        }
