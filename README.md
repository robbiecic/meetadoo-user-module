## About

This serverless micro service is supported by AWS API Gateway using Lambda proxy integration.

The service itself handles all user actions such as:

- Account Creation
- Account Validation
- Authentication
- Account updates
- Token issuer

### Devops

It's currently not built in docker, but may change in the future. It leverages AWS cloud-native services such as CloudFormation to describe the resources, and is managed by AWS CodePipeline, built by CodeBuild.

## How it works

1. User requests a new account. The account is stored separately until the email is validated then moved to a live account database
2. User logs in with provided email and password
3. If successful, Server responds with Set-Cookie HTTPONLY, Secure. This includes jwt_token encrypted with the email_address of the user.
4. When performing GET calls to the server, the jwt_token is stripped to get the email address of the user. This means the user is never stored on the client, only in the jwt stored within the browsers' HTTPS cookie

## Backlog

- Change action parameter to be a path instead
- Create login Audit. I.e. Date, IP Address, Email address. This can be displayed to the user if need be
- Create Audit of the API request being made. Could do this in cloud watch (Need a class to handle structure of cloud watch logs)
- Need to revisit the code that strips out the JWT token from the header
- Need to incorporate static code analysis and security scanners
- Build in a cache, particularly for isAuthenticated methods
- Need to label build number is available in code build
