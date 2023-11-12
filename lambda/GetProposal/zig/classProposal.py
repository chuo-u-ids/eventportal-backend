from boto3 import resource
import json

class Proposal:
    def __init__(self, json):
        self.id = json['id']
        self.presentationType = json['presentationType']
        self.title = json['title']
        self.abstract = json['abstract']
        self.estimated_time = json['estimated_time']
        self.seminar = json['seminar']
        self.speakers = json['speakers']

    def to_dict_for_post(self):
        return {
            'id': self.id,
            'presentationType': self.presentationType,
            'title': self.title,
            'abstract': self.abstract,
            'estimated_time': self.estimated_time,
            'seminar': self.seminar,
            'speakers': self.speakers
        }
    

    def to_dict(self):
        return {
            'id': self.id,
            'presentationType': self.presentationType,
            'title': self.title,
            'abstract': self.abstract,
            'estimated_time': int(self.estimated_time),
            'seminar': self.seminar,
            'speakers': self.speakers
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())
    
    def __str__(self):
        return self.to_json()
    
    def __repr__(self):
        return self.to_json()
    

class ProposalDb:
    def __init__(self, dyn_resource):
        self.dyn_resource = dyn_resource
        self.table = dyn_resource.Table('DynamoDbPresentationTable')

    def put(self, proposal):
        try:
            if self.get_by_title_and_type(proposal.title, proposal.presentationType) is not None:
                return {
                    "status": "ng",
                    "message": "The combination of title and presentationType must be unique",
                }
            self.table.put_item(Item=proposal.to_dict_for_post())
            return {
                "status": "ok",
                "presentationType": proposal.presentationType,
                "id": proposal.id,
                "title": proposal.title,
                "speakers": proposal.speakers,
            }
        except Exception as e:
            print(e)
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {
                        "status": "ng",
                        "message": str(e),
                    }
                ),
            }

    def get(self, id):
        response = self.table.get_item(Key={'id': id})
        if 'Item' not in response:
            return None
        return Proposal(response['Item'])
    
    def getall(self):
        # レコード全件吐き出し
        response = self.table.scan()
        if 'Items' not in response:
            return []
        return [Proposal(item) for item in response['Items']]
    
    def get_by_title_and_type(self, title, presentationType):
        response = self.table.scan(FilterExpression='title = :title and presentationType = :presentationType', ExpressionAttributeValues={':title': title, ':presentationType': presentationType})
        if response['Items'] == []:
            return None
        return [Proposal(item) for item in response['Items']]
    
    def get_by_title(self, title):
        response = self.table.scan(FilterExpression='title = :title', ExpressionAttributeValues={':title': title})
        if 'Items' not in response:
            return None
        return [Proposal(item) for item in response['Items']]
    
    def delete(self, title):
        self.table.delete_item(Key={'title': title})
        return {
            "status": "deleted",
            "title": title,
        }

    def update(self, proposal):
        self.table.update_item(Key={'title': proposal.title}, UpdateExpression='SET presentationType = :presentationType, abstract = :abstract, estimated_time = :estimated_time, seminar = :seminar, speakers = :speakers', ExpressionAttributeValues={':presentationType': proposal.presentationType, ':abstract': proposal.abstract, ':estimated_time': proposal.estimated_time, ':seminar': proposal.seminar, ':speakers': proposal.speakers})
        return {
            "status": "ok",
            "title": proposal.title,
            "presentationType": proposal.presentationType,
            "abstract": proposal.abstract,
            "estimated_time": proposal.estimated_time,
            "seminar": proposal.seminar,
            "speakers": proposal.speakers,
        }

    def scan(self):
        response = self.table.scan()
        if 'Items' not in response:
            return []
        return [Proposal(item) for item in response['Items']]
    
    def query(self, seminar):
        response = self.table.query(KeyConditionExpression='seminar = :seminar', ExpressionAttributeValues={':seminar': seminar})
        if 'Items' not in response:
            return []
        return [Proposal(item) for item in response['Items']]
    
    def query_by_speaker(self, speaker):
        response = self.table.scan(FilterExpression='contains(speakers, :speaker)', ExpressionAttributeValues={':speaker': speaker})
        if 'Items' not in response:
            return []
        return [Proposal(item) for item in response['Items']]
    
    def query_by_seminar(self, seminar):
        response = self.table.scan(FilterExpression='seminar = :seminar', ExpressionAttributeValues={':seminar': seminar})
        if 'Items' not in response:
            return []
        return [Proposal(item) for item in response['Items']]
    
    def query_by_speaker_and_seminar(self, speaker, seminar):
        response = self.table.scan(FilterExpression='contains(speakers, :speaker) and seminar = :seminar', ExpressionAttributeValues={':speaker': speaker, ':seminar': seminar})
        if 'Items' not in response:
            return []
        return [Proposal(item) for item in response['Items']]
    
    def query_by_speaker_and_seminar_and_type(self, speaker, seminar, presentationType):
        response = self.table.scan(FilterExpression='contains(speakers, :speaker) and seminar = :seminar and presentationType = :presentationType', ExpressionAttributeValues={':speaker': speaker, ':seminar': seminar, ':presentationType': presentationType})
        if 'Items' not in response:
            return []
        return [Proposal(item) for item in response['Items']]
    
    def query_by_speaker_and_type(self, speaker, presentationType):
        response = self.table.scan(FilterExpression='contains(speakers, :speaker) and presentationType = :presentationType', ExpressionAttributeValues={':speaker': speaker, ':presentationType': presentationType})
        if 'Items' not in response:
            return []
        return [Proposal(item) for item in response['Items']]

if __name__ == '__main__':
    dynamodb = resource('dynamodb')
    db = ProposalDb(dynamodb)
    print(db.getall())