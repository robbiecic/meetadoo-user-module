This is how the user API securely transmits and receives data:
1 - User logs in provided email and password (via https)
2 - If successful, Server responds with Set-Cookie HTTPONLY. This includes jwt_token encrypted with the email_address of the user
3 - When performing GET calls to the server, the jwt_token is stripped to get the email address of the user. This means the user is never stored on the client, only in the browser HTTP cookie


To-Do List:
1. Create login Audit. I.e. Date, IP Address, Email address. Could do this in cloud watch.
2. Create Audit of the API request being made. Could do this in cloud watch
3. Need a JWT validator. So when a 3rd party module (Minutes Module), receives a request to get data, it calls back here to check if the jwt is valid.