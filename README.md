# eventportal-backend

Eventportal Backend is the backend for Eventportal Web Apps.

## Dependencies
* [AWS SAM CLI](https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/install-sam-cli.html)
* Python3.11
* Packages defined with required.txt
* Firebase account (Spark plan is fine)

## How to run this server locally
With installing docker, you may use sam local command to test this app on local.

## How to deploy
You need to set those secrets on your GitHub's actions settings. You also need to permit run from github actions. We don't use access keys but just arn.
* `AWS_IAM_ARN_DEV`: AWS's IAM ARN which can deploy this SAM app.
* `AWS_STACK_NAME_DEV`: The stack name you wanna deploy this app.
* Firebase Service Account Info
  * `FIREBASE_PRIVATE_KEY_ID`
  * `FIREBASE_PRIVATE_KEY`
  * `FIREBASE_EMAIL`
  * `FIREBASE_CLIENT_EMAIL`
  * `FIREBASE_CLIENT_ID`
  * `FIREBASE_CLIENT_X509_CERT_URL`

On deploy, run the github action named `deploy`.

