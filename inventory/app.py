import os

from dynamoHandler.library import execute_statement
from eventHandler.library import process_result

EVENT_SOURCE = "Inventory"
EVENT_BUS = os.environ["EVENT_BUS"]
INVENTORY_TABLE = os.environ["INVENTORY_TABLE"]


def lambda_handler(event, context):
    eventType = event.get("detail-type")

    if eventType is not None:
        # EventBridge Invocation
        order = event.get("detail")

        if eventType == "OrderCreated":
            process_result(
                reserve_item(order["itemId"]),
                "ItemReserved",
                "ItemNotAvailable",
                order,
                "",
                EVENT_BUS,
                EVENT_SOURCE,
            )
        elif eventType == "PaymentFailed":
            process_result(
                unreserve_item(order["itemId"]),
                "ItemUnreserved",
                "ErrorItemUnreserved",
                order,
                "",
                EVENT_BUS,
                EVENT_SOURCE,
            )
        elif eventType == "PaymentMade":
            process_result(
                remove_reserved_item(order["itemId"]),
                "ItemRemoved",
                "ErrorItemRemoved",
                order,
                "",
                EVENT_BUS,
                EVENT_SOURCE,
            )
        elif eventType == "OrderCanceled":
            process_result(
                return_item_as_available(order["itemId"]),
                "ItemReturned",
                "ErrorItemReturned",
                order,
                "",
                EVENT_BUS,
                EVENT_SOURCE,
            )
        elif eventType == "ItemReserved":
            process_result(
                describe_item(order["itemId"]),
                "ItemDescribed",
                "ErrorItemDescribed",
                order,
                "item",
                EVENT_BUS,
                EVENT_SOURCE,
            )
        else:
            print(f"Event '{eventType}' not implemented.")


def describe_item(item_id):
    params = {
        "Statement": f"SELECT * FROM \"{INVENTORY_TABLE}\" WHERE itemId = '{item_id}'"
    }
    return execute_statement(params)


def reserve_item(item_id):
    params = {
        "Statement": f"UPDATE \"{INVENTORY_TABLE}\" SET available = available - 1, reserved = reserved + 1 WHERE itemId = '{item_id}' AND available > 0 RETURNING MODIFIED NEW *"
    }
    return execute_statement(params)


def unreserve_item(item_id):
    params = {
        "Statement": f"UPDATE \"{INVENTORY_TABLE}\" SET available = available + 1, reserved = reserved - 1 WHERE itemId = '{item_id}' AND reserved > 0 RETURNING MODIFIED NEW *"
    }
    return execute_statement(params)


def remove_reserved_item(item_id):
    params = {
        "Statement": f"UPDATE \"{INVENTORY_TABLE}\" SET reserved = reserved - 1 WHERE itemId = '{item_id}' AND reserved > 0 RETURNING MODIFIED NEW *"
    }
    return execute_statement(params)


def return_item_as_available(item_id):
    params = {
        "Statement": f"UPDATE \"{INVENTORY_TABLE}\" SET available = available + 1 WHERE itemId = '{item_id}' RETURNING MODIFIED NEW *"
    }
    return execute_statement(params)
