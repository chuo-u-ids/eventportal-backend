
import json
from firebase_admin import credentials, initialize_app, auth
from dotenv import load_dotenv
from boto3 import resource, client
from classUserinfo import Userinfo, UserinfoDb
import os

load_dotenv()
with open("firebase.json") as f:
    cred = credentials.Certificate(json.load(f))
app = initialize_app(credential=cred)


def lambda_handler(event, context):
    if event['httpMethod'] == 'OPTIONS':
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "status": "success",
                    "message": "Preflight"
                }
            ),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
        }
    headers = event['headers']
    if 'Authorization' not in headers:
        return {
            "statusCode": 401,
            "body": json.dumps(
                {
                    "status": "error",
                    "message": "Unauthorized"
                }
            ),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
        }
    else:
        token = headers['Authorization']
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        if uid is None:
            return {
                "statusCode": 401,
                "body": json.dumps(
                    {
                        "status": "error",
                        "message": "Unauthorized"
                    }
                ),
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                },
            }
    if UserinfoDb(resource('dynamodb')).get(uid) is None:
        return {
            "statusCode": 403,
            "body": json.dumps(
                {
                    "status": "error",
                    "message": "No User Data"
                }
            ),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
        }
    else:
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "status": "success",
                    "data": UserinfoDb(resource('dynamodb')).get(uid).to_json()
                }
            ),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
        }
