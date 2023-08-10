import json
import os
import random
import uuid

from dynamoHandler.library import execute_statement
from eventHandler.library import process_result

EVENT_SOURCE = "Payment"
EVENT_BUS = os.environ.get("EVENT_BUS")
PAYMENT_TABLE = os.environ.get("PAYMENT_TABLE")
PAYMENT_FAIL_PROBABILITY = float(os.environ.get("PAYMENT_FAIL_PROBABILITY", 0.0))


# Lambda Handler
def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    event_type = event.get("detail-type")

    if event_type is not None:
        # EventBridge Invocation
        order = event.get("detail")

        if event_type == "DeliveryEstimated":
            total_price = order["item"]["price"] + order["delivery"]["price"]
            payment_result = make_payment(total_price)
            process_result(
                payment_result,
                "PaymentMade",
                "PaymentFailed",
                order,
                "payment",
                EVENT_BUS,
                EVENT_SOURCE,
            )
        elif event_type == "ItemReturned":
            payment_id = order["order"]["paymentId"]
            payment_result = cancel_payment(payment_id)
            process_result(
                payment_result,
                "PaymentCanceled",
                "ErrorPaymentCanceled",
                order,
                "payment",
                EVENT_BUS,
                EVENT_SOURCE,
            )
        else:
            print(f"Event '{event_type}' not implemented.")


# Function to check if payment should fail
def should_payment_fail():
    return random.random() < PAYMENT_FAIL_PROBABILITY


# Function to make a payment
def make_payment(amount):
    payment_id = str(uuid.uuid4())
    failed = should_payment_fail()
    status = "FAILED" if failed else "PAID"

    params = {
        "Statement": f"INSERT INTO \"{PAYMENT_TABLE}\" VALUE {{'paymentId' : '{payment_id}', 'paymentMethod' : 'CREDIT_CARD', 'amount' : {amount}, 'status' : '{status}'}}"
    }
    execute_statement(params)

    return [
        {
            "paymentId": payment_id,
            "paymentMethod": "CREDIT_CARD",
            "amount": amount,
            "status": status,
        }
    ]


# Function to cancel a payment
def cancel_payment(payment_id):
    params = {
        "Statement": f"UPDATE \"{PAYMENT_TABLE}\" SET status = 'CANCELED' WHERE paymentId = '{payment_id}' AND status = 'PAID' RETURNING ALL NEW *"
    }

    payments = execute_statement(params)
    print(payments)

    return payments
