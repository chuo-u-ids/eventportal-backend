import json
from boto3 import resource, client
from classProposal import Proposal, ProposalDb
from uuid import uuid4
import os



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
    except Exception as e:
        return {
            "statusCode": 404,
            "body": json.dumps(
                {
                    "status": "not found",
                    "message": str(e),
                }
            ),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            }
        }
