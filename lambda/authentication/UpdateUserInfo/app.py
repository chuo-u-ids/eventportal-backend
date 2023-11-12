import json
from firebase_admin import credentials, initialize_app, auth
from dotenv import load_dotenv
from boto3 import resource, client
from zig.classUserinfo import Userinfo, UserinfoDb
import os

load_dotenv()
with open("firebase.json") as f:
    cred = credentials.Certificate(json.load(f))
app = initialize_app(cred)


def lambda_handler(event, context):
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
                    "message": "You have not registered"
                }
            ),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
        }
    else:
        body = json.loads(event['body'])
        db = UserinfoDb(resource('dynamodb'))
        user = db.get(body['id']).to_json()['email']
        user = Userinfo(
            id=body['id'],
            email=body['email'],
            name=body['name'],
            affiliation=body['affiliation'],
            department=body['department']
        )
        UserinfoDb(resource('dynamodb')).put_userinfo(user)
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "status": "success",
                    "message": "User Data",
                    "data": UserinfoDb(resource('dynamodb')).get(body['id']).to_json()
                }
            ),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
        }