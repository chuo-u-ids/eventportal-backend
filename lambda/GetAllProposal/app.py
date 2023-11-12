import json
from firebase_admin import credentials, initialize_app
from dotenv import load_dotenv
from boto3 import resource, client
from zig.classProposal import Proposal, ProposalDb


def lambda_handler(event, context):
    proposalDb = ProposalDb(resource('dynamodb', region_name='ap-northeast-1'))
    try:
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "status": "ok",
                    "item": [proposal.to_dict() for proposal in proposalDb.getall()]
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
