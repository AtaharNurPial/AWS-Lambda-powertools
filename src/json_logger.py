'''necessery dependencies for json logger'''
import logging
import os
from pythonjsonlogger import jsonlogger

'''powertool dependencies'''
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver

'''creating logger application named App'''
logger = logging.getLogger("Json_Logger_App")
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
    result = app.resolve(event, context)
    return result