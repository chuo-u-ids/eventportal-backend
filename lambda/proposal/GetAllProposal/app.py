import json
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
                    "item": [item.to_dict() for item in proposalDb.getall()]
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


if __name__ == "__main__":
    print(lambda_handler({}, {}))