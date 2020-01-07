
# cntl-alt-n - to start
# cntl-alt-m - to finish

import decimal
import json
from flask import Flask
import aws

app = Flask(__name__)

# Create dynamodb instance
dynamodb_client = aws.create_dynamodb_client()

user_table = dynamodb_client.table('dynamodb')


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/createUser')
def create_user():
    response = user_table.put_item(
        Item={
            'email_address': 'abs@gmail.com',
            'firstname': 'Robert',
            'surname': 'Cicero'
        }
    )
    return response


if __name__ == '__main__':
    app.run()
