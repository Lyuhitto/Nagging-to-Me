import json
from messages import messages


def lambda_handler(event, context):
    nagging()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def nagging():
    pass
