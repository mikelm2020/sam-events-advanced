import json
import os
import uuid
from datetime import datetime

from dynamoHandler.library import execute_statement
from eventHandler.library import process_result, send_event

EVENT_SOURCE = "Order"
EVENT_BUS = os.environ["EVENT_BUS"]
ORDER_TABLE = os.environ["ORDER_TABLE"]


def lambda_handler(event, context):
    result = []

    eventType = event.get("detail-type")

    if eventType is not None:
        # EventBridge Invocation
        order = event.get("detail")

        if eventType == "CreateOrder":
            create_order(order["customerId"], order["itemId"])
        elif eventType == "DeliveryWasDelivered":
            result = update_order("DELIVERED", order)
            process_result(
                result,
                "OrderDelivered",
                "ErrorOrderDelivered",
                order,
                None,
                EVENT_BUS,
                EVENT_SOURCE,
            )
        elif eventType == "DeliveryWasCanceled":
            result = update_order("DELIVERY_CANCELED", order)
            process_result(
                result,
                "OrderCanceled",
                "ErrorOrderCanceled",
                order,
                "order",
                EVENT_BUS,
                EVENT_SOURCE,
            )
        elif eventType == "PaymentMade":
            store_order("PAID", order)
        elif eventType == "PaymentFailed":
            store_order("PAYMENT_FAILED", order)
        elif eventType == "PaymentCanceled":
            update_order("PAYMENT_CANCELED", order)
        elif eventType == "DeliveryStarted":
            update_order("DELIVERING", order)
        else:
            print(f"Event '{eventType}' not implemented.")
    else:
        # API Gateway Invocation
        method = event["requestContext"]["http"]["method"]
        action = event["pathParameters"]["action"]
        customerId = event["pathParameters"]["customerId"]
        what = event["pathParameters"]["what"]

        if method == "GET":
            if action == "create":
                result = create_order(customerId, what)
            else:
                response = {
                    "statusCode": 501,
                    "body": f"Action '{action}' not implemented.",
                }
                return response

        response = {
            "statusCode": 200 if len(result) > 0 else 404,
            "body": json.dumps(result[0]) if len(result) > 0 else "Not Found",
        }

        return response


def create_order(customerId, itemId):
    print("create order")
    print(f"testing uuid {str(uuid.uuid4())}")

    orderId = datetime.now().isoformat()
    order = {"customerId": customerId, "orderId": orderId, "itemId": itemId}

    send_event("OrderCreated", order, EVENT_BUS, EVENT_SOURCE)
    print("event sent")
    return [order]


def store_order(orderStatus, order):
    orderDate = datetime.now().isoformat()
    db_order = {
        "customerId": order["customerId"],
        "orderId": order["orderId"],
        "orderStatus": orderStatus,
        "itemId": order["itemId"],
        "itemPrice": order["item"]["price"]["N"],
        "deliveryPrice": order["delivery"]["price"],
        "totalPrice": order["payment"]["amount"],
        "paymentId": order["payment"]["paymentId"],
        "deliveryAddress": order["customer"]["address"]["S"],
        "orderDate": orderDate,
        "updateDate": orderDate,
    }

    params = {"Statement": f'INSERT INTO \"{ORDER_TABLE}\" VALUE {db_order}'}

    execute_statement(params)


def update_order(orderStatus, order):
    updateDate = datetime.now().isoformat()
    params = {
        "Statement": f"UPDATE \"{ORDER_TABLE}\" SET orderStatus = '{orderStatus}', updateDate = '{updateDate}' WHERE customerId = '{order['customerId']}' AND orderId = '{order['orderId']}' RETURNING ALL NEW *"
    }
    updates = execute_statement(params)
    print(updates)
    return updates
