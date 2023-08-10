import boto3
from botocore.exceptions import ClientError

dynamodb_client = boto3.client('dynamodb')

def execute_statement(params):
    try:
        response = dynamodb_client.execute_statement(**params)
        items = response.get('Items', [])
        return items
    except ClientError as err:
        print(err)
        if err.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return []
        else:
            raise err
