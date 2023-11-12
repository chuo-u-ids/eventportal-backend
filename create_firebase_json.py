import json
import os
import sys

firebase_json = {
    "type": "service_account",
    "project_id": "chuo-u-eventportal",
    "private_key_id": os.environ.get("firebase_private_key_id"),
    "private_key": os.environ.get("firebase_private_key").replace("\\n", "\n"),
    "client_email": os.environ.get("firebase_client_email"),
    "client_id": os.environ.get("firebase_client_id"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.environ.get("firebase_client_x509_cert_url"),
    "universe_domain": "googleapis.com"
}

# export to each directory under /lambda/

dirs = [
    "lambda/authentication",
    "lambda/proposal",
]

for dir in dirs:
    files = os.listdir(dir)
    print(files)
    for file in files:
        with open(dir + "/" + file + "/firebase.json" , "w") as f:
            json.dump(firebase_json, f, indent=4)