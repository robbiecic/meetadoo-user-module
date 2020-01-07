import boto3
import json


def createClient():
    return boto3.client('sqs', region_name='us-east-2', aws_access_key_id="AKIARZLUVKQGALPFJIM4",
                        aws_secret_access_key="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")


def getSQSMessages(client, queue_url):

    # Receive message from SQS queue
    response = client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=1,
        VisibilityTimeout=2
    )

    # SQS will return a object of type messages if there is anything on the queue
    try:
        results = response['Messages']
    except Exception:
        results = 0

    return results


def sendMessage(client, messageBody):
    response = client.send_message(
        QueueUrl='https://sqs.us-east-2.amazonaws.com/123188106252/orders',
        MessageBody=json.dumps(messageBody),
        DelaySeconds=1,
        MessageAttributes={
            'Title': {
                'DataType': "String",
                'StringValue': "order"
            },
            'Author': {
                'DataType': "String",
                'StringValue': "algo"
            },
            'WeeksOn': {
                'DataType': "Number",
                'StringValue': "1"
            }
        }
    )
    return response


def sendSNS():
    client = boto3.client('sns', region_name='us-east-2', aws_access_key_id="AKIARZLUVKQGALPFJIM4",
                          aws_secret_access_key="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")

    response = client.publish(
        TopicArn='arn:aws:sns:us-east-2:123188106252:newTradeOrder',
        Message='RUN TRADING LAMBDA',
        Subject='RUN TRADING LAMBDA'
    )

    return response
