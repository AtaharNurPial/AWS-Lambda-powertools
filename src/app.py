# import json
import logging
import os
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver
from pythonjsonlogger import jsonlogger

'''creating logger application named App'''
logger = logging.getLogger("App")
'''declaring handler and formatter'''
logHandler = logging.StreamHandler()
#passing custom fields to the jsonFormatter
formatter = jsonlogger.JsonFormatter(fmt="%(asctime)s %(levelname)s %(name)s %(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
'''setting the logging level in the env_variable'''
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

app = ApiGatewayResolver()

@app.get("/activity/<month>")
def display_month(month):
    logger.info(f"Request for changing month to {month} received...")
    return{
        "message": f"Winter is coming in {month}...!!!"
    }

@app.get("/activity")
def display():
    logger.info("Message received...")
    return{
        "message": "winter is coming..."
    }

def lambda_handler(event, context):
    logger.debug(event)
    return app.resolve(event, context)

# def display(**kargs):
#     return {"statusCode": 200,
#      "body": json.dumps({"message": "winter is coming"})
#     }

# def display_month(event, **kargs):
#     month = event["pathParameters"]["month"]
#     return{
#         "status code": 200,
#         "body": json.dumps({
#             "message": f"Winter is coming in {month} ....!!!"
#         })
#     }

# class Router:
#     def __init__(self) -> None:
#         self.routes = {}

#     def set(self, path, method, handler):
#         self.routes[f"{path}-{method}"] = handler
    
#     def get(self, path, method):
#         try:
#             route = self.routes[f"{path}-{method}"]
#         except KeyError:
#             raise RuntimeError(f"Cannot route request to the correct method. path={path}, method={method}")
#         return route

# router = Router()
# router.set(path="/activity",method="GET", handler="display")
# router.set(path="/activity", method="GET", handler="display_month")

# def lambda_handler(event, context):
#     path = event["resource"]
#     http_method = event["httpMethod"]
#     method = router.get(path=path, method=http_method)
#     return method(event = event)
