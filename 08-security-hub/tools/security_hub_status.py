"""
Inspect the current AWS Security Hub status.

uv run tools/security_hub_status.py
"""

from pprint import pprint

import boto3
from botocore.exceptions import ClientError


def get_security_hub_status(client) -> dict:
    try:
        return client.describe_hub()
    except ClientError as error:
        return {
            "Error": error.response.get("Error", {}),
        }


def main() -> None:
    client = boto3.client("securityhub")
    response = get_security_hub_status(client)

    print("AWS Security Hub")
    print("=" * 50)
    print()
    print("Raw API Response")
    print("-" * 50)
    pprint(response)
    print()


if __name__ == "__main__":
    main()
