"""
Inspect the current AWS Security Hub status.

uv run tools/security_hub_status.py
"""

from pprint import pprint

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


def get_standard_controls(
    client,
    standards_subscription_arn: str,
) -> dict:
    try:
        return client.describe_standards_controls(
            StandardsSubscriptionArn=standards_subscription_arn,
        )
    except ClientError as error:
        return {
            "Error": error.response.get("Error", {}),
        }


def inspect_standard_controls(
    client,
    standards_subscription_arn: str,
) -> None:
    response = get_standard_controls(
        client,
        standards_subscription_arn,
    )

    controls = response.get("Controls", [])

    print(f"Controls: {len(controls)}")
    print()

    if controls:
        print("Sample Control")
        print("-" * 50)
        pprint(controls[0])
        print()


def main() -> None:
    client = boto3.client("securityhub")

    status_response = get_security_hub_status(client)
    standards_response = get_enabled_standards(client)

    print_security_hub_status(
        status_response,
        standards_response,
    )

    print("Security Controls")
    print("=" * 50)
    print()

    for subscription in standards_response.get(
        "StandardsSubscriptions",
        [],
    ):
        subscription_arn = subscription.get("StandardsSubscriptionArn")

        if subscription_arn:
            inspect_standard_controls(
                client,
                subscription_arn,
            )


if __name__ == "__main__":
    main()
