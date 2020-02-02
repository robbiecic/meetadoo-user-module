This is how the user API securely transmits and receives data:


1 - User logs in provided email and password (via https)
2 - If successful, Server responds with Set-Cookie HTTPONLY. This includes jwt_token encrypted with the email_address of the user
3 - When performing GET calls to the server, the jwt_token is stripped to get the email address of the user. This means the user is never stored on the client, only in the browser HTTP cookie
