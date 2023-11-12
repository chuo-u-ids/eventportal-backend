import json
from firebase_admin import credentials, initialize_app
from dotenv import load_dotenv
from boto3 import resource, client
from zig.classProposal import Proposal, ProposalDb
from uuid import uuid4
import os

load_dotenv()

def lambda_handler(event, context):
    data = json.loads(event['body'])
    data['id'] = uuid4().hex
    proposal = Proposal(data)
    proposalDb = ProposalDb(resource('dynamodb', region_name='ap-northeast-1'))
    return proposalDb.put(proposal)
