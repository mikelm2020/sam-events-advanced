import json
import os

from dynamoHandler.library import execute_statement
from eventHandler.library import process_result
from locationHandler.library import (get_place_from_address,
                                     get_route_for_address)

# Global variable for startAddressPlace
start_address_place = None

# Constants from environment variables
EVENT_SOURCE = "Delivery"
EVENT_BUS = os.environ.get("EVENT_BUS")
PLACE_INDEX = os.environ.get("PLACE_INDEX")
ROUTE_CALCULATOR = os.environ.get("ROUTE_CALCULATOR")
DELIVERY_TABLE = os.environ.get("DELIVERY_TABLE")
START_ADDRESS = "60 Holborn Viaduct, London EC1A 2FD, UK"


# Lambda Handler
def lambda_handler(event, context):
    if start_address_place is None:
        start_address_place = get_place_from_address(START_ADDRESS, PLACE_INDEX)

    event_type = event.get("detail-type")

    if event_type is not None:
        # EventBridge Invocation
        order = event.get("detail")

        if event_type == "CustomerDescribed":
            address = order.get("customer").get("address")
            if address:
                delivery_result = estimate_delivery(address)
                process_result(
                    delivery_result,
                    "DeliveryEstimated",
                    "ErrorDeliveryEstimated",
                    order,
                    "delivery",
                    EVENT_BUS,
                    EVENT_SOURCE,
                )
            else:
                print("No address provided in the event.")
        elif event_type == "ItemRemoved":
            customer_id = order.get("customerId")
            order_id = order.get("orderId")
            address = order.get("customer").get("address")
            if customer_id and order_id and address:
                mark_delivery_result = mark_delivery_as_started(
                    customer_id, order_id, address
                )
                process_result(
                    mark_delivery_result,
                    "DeliveryMarkedAsStarted",
                    "ErrorMarkDeliveryAsStarted",
                    order,
                    "delivery",
                    EVENT_BUS,
                    EVENT_SOURCE,
                )
            else:
                print("Incomplete order information provided in the event.")
        elif event_type == "Delivered":
            customer_id = order.get("customerId")
            order_id = order.get("orderId")
            if customer_id and order_id:
                delivered_result = delivered(customer_id, order_id)
                process_result(
                    delivered_result,
                    "DeliveryWasDelivered",
                    "ErrorDeliveryWasDelivered",
                    order,
                    "delivery",
                    EVENT_BUS,
                    EVENT_SOURCE,
                )
            else:
                print("Incomplete order information provided in the event.")
        elif event_type == "DeliveryCanceled":
            customer_id = order.get("customerId")
            order_id = order.get("orderId")
            if customer_id and order_id:
                cancel_delivery_result = cancel_delivery(customer_id, order_id)
                process_result(
                    cancel_delivery_result,
                    "DeliveryWasCanceled",
                    "ErrorDeliveryWasCanceled",
                    order,
                    "delivery",
                    EVENT_BUS,
                    EVENT_SOURCE,
                )
            else:
                print("Incomplete order information provided in the event.")
        else:
            print(f"Event '{event_type}' not implemented.")


# Lambda DLQ Handler
def delivery_dlq_handler(event, context):
    print("Delivery DLQ function")
    print(event)

    body = json.loads(event["Records"][0]["body"])
    order = body.get("detail")

    if order:
        print(order)
        process_result(
            cancel_delivery(order.get("customerId"), order.get("orderId")),
            "DeliveryWasCanceled",
            "ErrorDeliveryWasCanceled",
            order,
            "delivery",
            EVENT_BUS,
            EVENT_SOURCE,
        )
    else:
        print("No order details found in the DLQ event.")


# Function to estimate delivery
def estimate_delivery(address):
    route_summary = get_route_summary_for(address)
    return [route_summary]


# Function to mark delivery as started
def mark_delivery_as_started(customer_id, order_id, address):
    delivery_status = "DELIVERING"
    route_summary = get_route_summary_for(address)

    # DynamoDB Item
    delivery_item = {
        "customerId": customer_id,
        "orderId": order_id,
        "address": address,
        "deliveryStatus": delivery_status,
        "price": str(route_summary.get("price")),
    }
    params = {"Statement": f'INSERT INTO"{DELIVERY_TABLE}" VALUE {delivery_item}'}
    execute_statement(params)

    return [
        {
            "customerId": customer_id,
            "orderId": order_id,
            "address": address,
            "deliveryStatus": delivery_status,
        }
    ]


# Function to cancel a delivery
def cancel_delivery(customer_id, order_id):
    params = {
        "Statement": f"UPDATE \"{DELIVERY_TABLE}\" SET deliveryStatus = 'CANCELED' WHERE customerId = '{customer_id}' AND orderId = '{order_id}' RETURNING MODIFIED NEW *"
    }
    updates = execute_statement(params)
    return updates


def delivered(customer_id, order_id):
    params = {
        "Statement": f"UPDATE \"{DELIVERY_TABLE}\" SET deliveryStatus = 'DELIVERED' WHERE customerId = '{customer_id}' AND orderId = '{order_id}' RETURNING MODIFIED NEW *"
    }
    updates = execute_statement(params)
    return updates


def get_route_summary_for(address):
    route = get_route_for_address(
        address, start_address_place, PLACE_INDEX, ROUTE_CALCULATOR
    )
    route_summary = route.get("Summary", {})

    duration_seconds = route_summary.get("DurationSeconds", 0)
    route_summary["price"] = round(duration_seconds / 100, 2)  # Redondear precio

    return route_summary
