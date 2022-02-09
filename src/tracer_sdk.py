'''tracer dependency'''
from aws_xray_sdk.core import xray_recorder,patch_all
'''powertool dependencies'''
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver
from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging import correlation_paths

#adding powertool logger.
logger = Logger(service = "Powertool_Logger_App")

app = ApiGatewayResolver()

cold_start = True
'''patch_all() -> ingores any libraries that are not installed'''
patch_all() 

@app.get("/activity/<month>")
@xray_recorder.capture('display_month')
def display_month(month):
    subsegment = xray_recorder.current_subsegment()
    subsegment.put_annotation(key = "User", value = month)
    logger.info(f"Request for changing month to {month} received...")
    return{
        "message": f"Winter is coming in {month}...!!!"
    }

@app.get("/activity")
@xray_recorder.capture('display')
def display():
    subsegment = xray_recorder.current_subsegment()
    subsegment.put_annotation(key = "User", value = "Message")
    logger.info("Message received...")
    return{
        "message": "winter is coming..."
    }

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
