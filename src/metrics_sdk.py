'''necessery dependencies for metrics'''
import os
import boto3

'''powertool dependencies'''
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.logging import correlation_paths

cold_start = True
# '''creating a container for all metrics'''
metric_namespace = "MyApp"

#adding powertool logger.
logger = Logger(service = "Powertool_Logger_App")
#adding powertool tracer
tracer = Tracer(service = "Powertool_Tracer_App")
# cloudwatch client initialized
metrics = boto3.client( "cloudwatch")

app = ApiGatewayResolver()


'''custom metrics generator'''
@tracer.capture_method
def add_greeting_metric(service: str = "Metric_App"):
    function_name = os.getenv("AWS_LAMBDA_FUNCTION_NAME", "undefined")
    service_dimension = {"Name": "service", "Value": service}
    function_dimension = {"Name": "function_name", "Value": function_name}
    is_cold_start = True

    global cold_start
    if cold_start:
        cold_start = False
    else:
        is_cold_start = False

    return metrics.put_metric_data(
        MetricData = [
            {
                "MetricName": "SuccessfullGreetings",
                "Dimensions": [service_dimension],
                "Unit": "Count",
                "Value": 1,
            },
            {
                "MetricName": "ColdStart",
                "Dimensions": [service_dimension, function_dimension],
                "Unit": "Count",
                "Value": int(is_cold_start)
            }
        ],
        Namespace = metric_namespace,
    )

@app.get("/activity/<month>")
@tracer.capture_method
def display_month(month):
    tracer.put_annotation(key = "User", value = month)
    logger.info(f"Request for changing month to {month} received...")
    add_greeting_metric()
    return{
        "message": f"Winter is coming in {month}...!!!"
    }

@app.get("/activity")
def display():
    tracer.put_annotation(key = "User", value = "Message")
    logger.info("Message received...")
    add_greeting_metric()
    return{
        "message": "winter is coming..."
    }

@logger.inject_lambda_context(correlation_id_path = correlation_paths.API_GATEWAY_REST, log_event = True)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    result = app.resolve(event, context)
    return result
