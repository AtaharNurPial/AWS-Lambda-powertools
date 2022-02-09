'''powertool dependencies'''
from typing import List
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.middleware_factory import lambda_handler_decorator

#adding powertool logger.
logger = Logger(service = "Powertool_Logger_App")
#adding powertool tracer
tracer = Tracer(service = "Powertool_Tracer_App")
# adding powertool metric generator
metrics = Metrics(namespace="Myapp", service= "Powertool_Metric_App")

app = ApiGatewayResolver()

'''creating middleware'''
@lambda_handler_decorator(trace_execution= True)
def middleware_before_after(handler, event, context):
    #logic_before_handler_execution()
    print("Saying hello before Handler is called...")
    response = handler(event, context)
    #logic_after_handler_execution()
    print("saying hello after Handler is called...")
    return response

@lambda_handler_decorator(trace_execution= True)
def hiding_sensitive_data(handler, event, context, fields: List = None):
    tracer = Tracer()
    tracer.put_annotation(key= "user", value= "Message")
    if fields:
        for field in fields:
            if field in event:
                event[field] = obfuscate(event[field])
    return handler(event, context)

@lambda_handler_decorator(trace_execution= True)
def another_middleware(handler, event, context, hello = False ):
    if hello:
        print("------ Parameter Detected ------")
    print("Saying hello before Handler is called")
    response = handler(event, context)
    print("Saying hello after Handle is called")
    return response

'''routing decorator next tracer decorator'''
@app.get("/activity/<month>")
@tracer.capture_method
def display_month(month):
    tracer.put_annotation(key = "User", value = month)
    logger.info(f"Request for changing month to {month} received...")
    metrics.add_metric(name = "SuccessfulGreeting", unit = MetricUnit.Count, value = 1)
    return{
        "message": f"Winter is coming in {month}...!!!"
    }
    
'''routing decorator then tracer decorator'''
@app.get("/activity")
def display():
    tracer.put_annotation(key = "User", value = "Message")
    logger.info("Message received...")
    metrics.add_metric(name="SuccessfulGreeting",unit=MetricUnit.Count,value=1)
    # add_greeting_metric()
    return{
        "message": "winter is coming..."
    }

'''using logger.inject_lambda_context decorator to inject key 
information from Lambda context into every log.
also setting log_event=True to automatically log each incoming request for debugging'''
@logger.inject_lambda_context(correlation_id_path = correlation_paths.API_GATEWAY_REST, log_event = True)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
@middleware_before_after
@hiding_sensitive_data(fields=["email"])
@another_middleware(hello=True)
def lambda_handler(event, context):
    result = app.resolve(event, context)
    try:
        return result
    except Exception as e:
        logger.exception(e)
        raise