import json
import tweepy
import random
import boto3
from messages import messages


ssm = boto3.client('ssm', region_name='ap-northease-2')


def authenticate_twitter():
    consumer_key = (
        ssm.get_parameter(Name='nag-consumer-key', WithDecryption=True)
        )['Parameter']['Value']
    consumer_secret = (
        ssm.get_parameter(Name='nag-consumer-key-secret', WithDecryption=True)
        )['Parameter']['Value']
    access_token = (
        ssm.get_parameter(Name='nag-access-token', WithDecryption=True)
        )['Parameter']['Value']
    access_secret = (
        ssm.get_parameter(Name='nag-access-token-secret', WithDecryption=True)
        )['Parameter']['Value']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(
        auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True
        )

    return api


def nagging(api):
    message = random.choice(messages)
    api.update_status(status=message)


def lambda_handler(event, context):
    try:
        api = authenticate_twitter()
        nagging(api)
        print('now nagging!')
    except Exception as e:
        print(e)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
