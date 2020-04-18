## About

This micro service handles all user actions such as:

- Account Creation
- Account Validation
- Authentication
- Account updates
- Token issuer

## How it works

1. User logs in provided email and password (via https)
2. If successful, Server responds with Set-Cookie HTTPONLY. This includes jwt_token encrypted with the email_address of the user
3. When performing GET calls to the server, the jwt_token is stripped to get the email address of the user. This means the user is never stored on the client, only in the browser HTTPS cookie

## Backlog

- Might need a class to handle structure of cloud watch logs
- Create login Audit. I.e. Date, IP Address, Email address. This can be displayed to the user if need be
- Create Audit of the API request being made. Could do this in cloud watch
- Need an email verification step
- Need email alerts
- Need to revisit the code that strips out the JWT token from the header
- Need to label build versions better
- Need to incorporate static code analysis and security scanners
