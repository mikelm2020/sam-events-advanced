import os
import json
import boto3
import datetime

store_table = os.environ['STORE_TABLE']

dynamodb_client = boto3.client('dynamodb')
dynamodb_doc_client = boto3.resource('dynamodb')
ddb_doc = dynamodb_doc_client.Table(store_table)

def lambda_handler(event, context):
    print(json.dumps(event, indent=2))
    store_event(event)

def store_event(event):
    current_time = int(datetime.datetime.now().timestamp())  # event.time is express in seconds and not ms, not enough precision
    
    who = 'C#' + event['detail']['customerId'] # C# for customers, P# for products, ...
    time_what = f"{current_time}#{event['detail-type']}"
    event_detail = json.dumps(event['detail'])

    db_event = f"{{'who': '{who}', 'timeWhat': '{time_what}', 'eventSource': '{event['source']}', 'eventDetail': '{event_detail}'}}"
    params = {
        "Statement": f"INSERT INTO \"{store_table}\" VALUE {db_event}"
    }

    print(params)

    try:
        items = dynamodb_client.execute_statement(**params)
        return items
    except Exception as e:
        print(e)

