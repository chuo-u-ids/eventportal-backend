import json

from boto3 import resource


class Userinfo:
    def __init__(self, json):
        self.email = json["email"]
        self.name = json["name"]
        self.affiliation = json["affiliation"]
        self.department = json["department"]
        self.uid = json["uid"]

    def to_json(self):
        return {
            "uid": self.uid,
            "email": self.email,
            "name": self.name,
            "affiliation": self.affiliation,
            "department": self.department,
        }


class UserinfoDb:
    def __init__(self, dynamodb_resource):
        self.table = dynamodb_resource.Table("DynamoDbAccountTable")

    def get(self, uid):
        response = self.table.get_item(Key={"uid": uid})
        if "Item" not in response:
            return None
        return Userinfo(response["Item"])

    def get_userinfo(self, email):
        response = self.table.scan()
        if "Items" not in response:
            return None
        for item in response["Items"]:
            if item["email"] == email:
                return Userinfo(item)
        return None

    def put(self, userinfo):
        self.table.put_item(Item=userinfo.to_json())

    def update(self, userinfo):
        self.table.update_item(
            Key={"uid": userinfo.uid},
            UpdateExpression="set email=:e, name=:n, affiliation=:a, department=:d",
            ExpressionAttributeValues={
                ":e": userinfo.email,
                ":n": userinfo.name,
                ":a": userinfo.affiliation,
                ":d": userinfo.department,
            },
            ReturnValues="UPDATED_NEW",
        )
