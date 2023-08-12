import json
import os

from dynamoHandler.library import execute_statement
from eventHandler.library import process_result

# Constants from environment variables
EVENT_SOURCE = "Customer"
EVENT_BUS = os.environ.get("EVENT_BUS")
CUSTOMER_TABLE = os.environ.get("CUSTOMER_TABLE")


# Lambda Handler
def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    event_type = event.get("detail-type")

    if event_type is not None:
        # EventBridge Invocation
        order = event.get("detail")

        if event_type == "ItemDescribed":
            customer_id = order.get("customerId")
            if customer_id:
                customer_description = describe_customer(customer_id)
                if customer_description:
                    process_result(
                        customer_description,
                        "CustomerDescribed",
                        "ErrorCustomerDescribed",
                        order,
                        "customer",
                        EVENT_BUS,
                        EVENT_SOURCE,
                    )
                else:
                    print(f"Customer with ID {customer_id} not found.")
            else:
                print("No customerId provided in the event.")
        else:
            print(f"Event '{event_type}' not implemented.")


# Function to describe a customer
def describe_customer(customer_id):
    params = {
        "Statement": f"SELECT * FROM \"{CUSTOMER_TABLE}\" WHERE customerId = '{customer_id}'"
    }

    return execute_statement(params)
