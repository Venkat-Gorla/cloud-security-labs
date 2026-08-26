"""
Inspect the current AWS Security Hub status.

uv run tools/security_hub_status.py
"""

import boto3
from botocore.exceptions import ClientError

from output import print_security_hub_status


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

    print_security_hub_status(
        status_response,
        standards_response,
    )


if __name__ == "__main__":
    main()
