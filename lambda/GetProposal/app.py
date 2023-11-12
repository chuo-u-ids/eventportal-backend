import json
from firebase_admin import credentials, initialize_app
from dotenv import load_dotenv
from boto3 import resource, client
from zig.classProposal import Proposal, ProposalDb
from uuid import uuid4
import os

load_dotenv()

def lambda_handler(event, context):
    id = event['pathParameters']['id']
    proposalDb = ProposalDb(resource('dynamodb', region_name='ap-northeast-1'))
    try:
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "status": "ok",
                    "item": proposalDb.get(id).to_dict()
                }
            ),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
        }
    except:
        return {
            "statusCode": 404,
            "body": json.dumps(
                {
                    "status": "not found",
                }
            ),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            }
        }