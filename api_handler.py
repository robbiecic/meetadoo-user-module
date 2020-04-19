from user_functions import create_user, remove_user, login, get_user, isAuthenticated, update_user, get_user_list, set_expired_cookie, validate_email


class API_Handler:

    def __init__(self, queryStringParameters: dict, httpMethod: str, body: dict, header: dict):
        self.queryStringParameters = queryStringParameters
        self.action = queryStringParameters['action']
        self.httpMethod = httpMethod
        self.body = body
        self.header = header
        self.jwt = self.get_jwt()
        self.authenticated_response = self.is_authenticated()

    def get_email(self):
        if 'email' in self.body.keys():
            return self.body['email']
        else:
            return ''

    def run_action(self):
        # Declare all method endpoints
        if self.action == 'CreateUser' and self.httpMethod == 'POST':
            return self.create_user()
        elif self.action == 'Login' and self.httpMethod == 'POST':
            return self.login()
        elif self.action == 'isAuthenticated' and self.httpMethod == 'GET':
            return self.isAuthenticated()
        elif self.action == 'ConfirmEmail' and self.httpMethod == 'GET':
            return self.confirm_email()
        elif self.action == 'Logout' and self.httpMethod == 'POST' and self.authenticated_response:
            return self.logout()
        elif self.action == 'RemoveUser' and self.httpMethod == 'POST' and self.authenticated_response:
            return self.remove_user()
        elif self.action == 'getUser' and self.httpMethod == 'GET' and self.authenticated_response:
            return self.getUser()
        elif self.action == 'getUserList' and self.httpMethod == 'GET' and self.authenticated_response:
            return self.getUserList()
        elif self.action == 'UpdateUser' and self.httpMethod == 'POST' and self.authenticated_response:
            return self.updateUser()
        else:
            return {
                'statusCode': 400,
                'body': "A valid request action was not provided"
            }

    def confirm_email(self):
        result = validate_email(
            self.queryStringParameters['email'], self.queryStringParameters['token'])
        # Redirect to register page after, need to think about passing success and fail messages here
        header = {}
        header["Location"] = 'https://www.meetadoo.com/#/register'
        return {
            "headers": header,
            'statusCode': result['statusCode'],
            'body': result['response']
        }

    def isAuthenticated(self):
        result = isAuthenticated(self.jwt)
        return {
            'statusCode': result['statusCode'],
            'body': result['response']
        }

    def updateUser(self):
        result = update_user(self.body['data'])
        return {
            'statusCode': result['statusCode'],
            'body': result['response']
        }

    def getUserList(self):
        result = get_user_list()
        return {
            'statusCode': result['statusCode'],
            'body': result['response']
        }

    def getUser(self):
        # Get email from decoded response. Don't want to store it on client side, but it's in the token which is issued upon successful login
        body_email = self.authenticated_response
        result = get_user(body_email)
        return {
            'headers': {},
            'statusCode': result['statusCode'],
            'body': result['response']
        }

    def logout(self):
        expired_cookie = set_expired_cookie()
        header = {}
        header["Set-Cookie"] = expired_cookie
        return {
            "headers": header,
            'statusCode': "200",
            'body': "You are now logged out"
        }

    def login(self):
        result = login(self.body['data'])
        header = {}
        header["Set-Cookie"] = result['cookie']
        return {
            "headers": header,
            'statusCode': result['statusCode'],
            'body': result['response']
        }

    def remove_user(self):
        result = remove_user(self.get_email())
        return {
            'statusCode': result['statusCode'],
            'body': result['response']
        }

    def create_user(self):
        result = create_user(self.body['data'])
        return {
            'statusCode': result['statusCode'],
            'body': result['response']
        }

    def get_jwt(self):
        # Locate cookie details if there, if not ignore
        jwt_token = "Something Invalid"
        try:
            # 'cookie' is case sensistive. Is lower case from browser, upper care from Postman
            try:
                cookie = self.header['cookie']
            except:
                cookie = self.header['Cookie']
            print('Cookie - ' + str(cookie))
            # Had to add this as running through AWS, different cookies are added. We want the one starting with jwt
            split_cookie = str(cookie).split(';')
            for x in split_cookie:
                try:
                    index = str(x).index("jwt")
                    jwt_token = x.replace("jwt", "").replace(
                        " ", "").replace("=", "")
                    return jwt_token
                except:
                    # Ignore, index will throw an error meaning the "jwt" doesn't exist
                    pass
        except:
            return "Something Invalid"

    def is_authenticated(self):
        authenticated_response = isAuthenticated(self.jwt)
        if authenticated_response['statusCode'] == 200:
            return authenticated_response['response']
        return False
