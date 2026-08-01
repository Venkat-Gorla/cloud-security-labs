"""
Read an item from the Config Lab DynamoDB table.
"""

import os
import boto3

TABLE_NAME = os.environ["TABLE_NAME"]
table = boto3.resource("dynamodb").Table(TABLE_NAME)


def lambda_handler(event, context):
    item_id = event.get("id")
    if not item_id:
        return {
            "statusCode": 400,
            "body": "Missing required field: id",
        }

    response = table.get_item(
        Key={
            "id": item_id,
        }
    )

    item = response.get("Item")
    if item is None:
        return {
            "statusCode": 404,
            "body": "Item not found",
        }

    return {
        "statusCode": 200,
        "body": item,
    }
