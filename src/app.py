import json


def hello():
    return {"statusCode": 200,
     "body": json.dumps({"message": "winter is coming"})
    }


def lambda_handler(event, context):
    return hello()
