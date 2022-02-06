# import json
'''necessery dependencies for json logger'''
# import logging
# import os
# from pythonjsonlogger import jsonlogger
'''tracer dependency'''
from unittest import result
from aws_xray_sdk.core import xray_recorder,patch_all
'''powertool dependencies'''
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver
from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging import correlation_paths


#adding powertool logger.
logger = Logger(service = "Powertool_Logger_App")
'''Don't need to use any of these if we use powertool logger....'''
'''creating logger application named App'''
# logger = logging.getLogger("Json_Logger_App")
# '''declaring handler and formatter'''
# logHandler = logging.StreamHandler()
# #passing custom fields to the jsonFormatter
# formatter = jsonlogger.JsonFormatter(fmt="%(asctime)s %(levelname)s %(name)s %(message)s")
# logHandler.setFormatter(formatter)
# logger.addHandler(logHandler)
# '''setting the logging level in the env_variable'''
# logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

app = ApiGatewayResolver()
cold_start = True
patch_all()

'''routing decorator then tracer decorator'''
@app.get("/activity/<month>")
@xray_recorder.capture('display_month')
def display_month(month):
    subsegment = xray_recorder.current_subsegment()
    subsegment.put_annotation(key = "User", value = month)
    logger.info(f"Request for changing month to {month} received...")
    return{
        "message": f"Winter is coming in {month}...!!!"
    }
    
'''routing decorator then tracer decorator'''
@app.get("/activity")
@xray_recorder.capture('display')
def display():
    subsegment = xray_recorder.current_subsegment()
    subsegment.put_annotation(key = "User", value = "Message")
    logger.info("Message received...")
    return{
        "message": "winter is coming..."
    }

'''using logger.inject_lambda_context decorator to inject key 
information from Lambda context into every log.
also setting log_event=True to automatically log each incoming request for debugging'''
@logger.inject_lambda_context(correlation_id_path = correlation_paths.API_GATEWAY_REST, log_event = True)
@xray_recorder.capture('handler')
def lambda_handler(event, context):
    global cold_start
    subsegment = xray_recorder.current_subsegment()
    if cold_start:
        subsegment.put_annotation(key = "ColdStart", value = cold_start)
        cold_start = False
    else:
        subsegment.put_annotation(key = "ColdStart", value = cold_start)
    logger.debug(event)
    result = app.resolve(event, context)
    subsegment.put_metadata("response", result)
    return result

#don't need any of these if we use powertools for api routing... SOOO EASY!!!!!
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
