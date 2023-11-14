import json
from firebase_admin import credentials, initialize_app, auth
from dotenv import load_dotenv
from boto3 import resource, client
from classProposal import Proposal, ProposalDb
from classUserinfo import Userinfo, UserinfoDb
from uuid import uuid4
import os

load_dotenv()
with open("firebase.json") as f:
    cred = credentials.Certificate(json.load(f))
app = initialize_app(cred)


def lambda_handler(event, context):

    # check token stored in header and get email address from the token
    # if not authorized, return 401
    # if authorized, get email address from token
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
        user_db = UserinfoDb(resource('dynamodb', region_name='ap-northeast-1'))
        user = user_db.get(uid)
        email = user.email
        if email is None:
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

    data = json.loads(event['body'])
    data['id'] = uuid4().hex
    data['applicant'] = email
    proposal = Proposal(data)
    proposalDb = ProposalDb(resource('dynamodb', region_name='ap-northeast-1'))
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "status": "ok",
                "item": proposalDb.put(proposal),
            }
        ),
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
    }
