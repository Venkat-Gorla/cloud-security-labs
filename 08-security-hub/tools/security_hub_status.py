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


def get_enabled_standards(client) -> dict:
    try:
        return client.get_enabled_standards()
    except ClientError as error:
        return {
            "Error": error.response.get("Error", {}),
        }


def main() -> None:
    client = boto3.client("securityhub")

    status_response = get_security_hub_status(client)
    standards_response = get_enabled_standards(client)

    print("AWS Security Hub")
    print("=" * 50)
    print()

    print("Hub Status")
    print("-" * 50)
    pprint(status_response)
    print()

    print("Enabled Standards")
    print("-" * 50)
    pprint(standards_response)
    print()


if __name__ == "__main__":
    main()
