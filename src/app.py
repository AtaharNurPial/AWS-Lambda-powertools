import json

def display(days):
    return{
        "status code": 200,
        "body": json.dumps({
            "message": f"Winter is coming in {days} days!!!"
        })
    }

def lambda_handler(event, context):
    days = event["pathPaameters"]["days"]
    return display(days)