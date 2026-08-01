"""
Populate the Config Lab DynamoDB table.

uv run src/populate.py
"""

import boto3

TABLE_NAME = "cloud-security-config-lab-table"

ITEMS = [
    {
        "id": "1001",
        "name": "Alice",
        "department": "Sales",
    },
    {
        "id": "1002",
        "name": "Bob",
        "department": "Engineering",
    },
    {
        "id": "1003",
        "name": "Charlie",
        "department": "Finance",
    },
    {
        "id": "1004",
        "name": "Diana",
        "department": "HR",
    },
    {
        "id": "1005",
        "name": "Ethan",
        "department": "Marketing",
    },
]


def main() -> None:
    table = boto3.resource("dynamodb").Table(TABLE_NAME)

    print(f"Loading {len(ITEMS)} items into {TABLE_NAME}...")

    with table.batch_writer() as batch:
        for item in ITEMS:
            batch.put_item(Item=item)

    print("Done.")


if __name__ == "__main__":
    main()
