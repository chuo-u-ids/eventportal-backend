import json
from firebase_admin import credentials, initialize_app, auth
from dotenv import load_dotenv
from boto3 import resource, client
from classUserinfo import Userinfo, UserinfoDb
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
    if UserinfoDb(resource('dynamodb')).get(uid) is not None:
        return {
            "statusCode": 403,
            "body": json.dumps(
                {
                    "status": "error",
                    "message": "You have already registered. Please update from update function."
                }
            ),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
        }
    else:
        userdb = UserinfoDb(resource('dynamodb'))
        body = json.loads(event['body'])
        user = Userinfo(
            json={
                'uid': decoded_token['uid'],
                'email': body['email'],
                'name': body['name'],
                'affiliation': body['affiliation'],
                'department': body['department']
            }
        )
        try:
            userdb.put(user)
            return {
                "statusCode": 200,
                "body": json.dumps(
                    {
                        "status": "success",
                        "data": user.to_json()
                    }
                ),
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                },
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps(
                    {
                        "status": "error",
                        "message": "Internal Server Error",
                        "error": str(e)
                    }
                ),
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                },
            }