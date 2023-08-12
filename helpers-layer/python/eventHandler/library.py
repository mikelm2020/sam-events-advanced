import json

import boto3

eventbridge_client = boto3.client("events")


def process_result(result, OK, KO, output, add, bus_name, event_source):
    if result:
        if add is not None:
            output[add] = result[0]
        send_event(OK, output, bus_name, event_source)
    else:
        send_event(KO, output, bus_name, event_source)


def send_event(event_type, event_detail, bus_name, event_source):
    params = {
        "Entries": [
            {
                "Detail": json.dumps(event_detail),
                "DetailType": event_type,
                "EventBusName": bus_name,
                "Source": event_source,
            }
        ]
    }
    response = eventbridge_client.put_events(Entries=params["Entries"])
    return response
