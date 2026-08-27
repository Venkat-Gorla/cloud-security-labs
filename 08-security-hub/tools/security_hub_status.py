"""
Inspect the current AWS Security Hub status.

uv run tools/security_hub_status.py
"""

from pathlib import Path
import boto3
from botocore.exceptions import ClientError
from output import print_security_hub_status
from security_hub_analysis import save_findings


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
        paginator = client.get_paginator("describe_standards_controls")
        controls = []

        for page in paginator.paginate(
            StandardsSubscriptionArn=standards_subscription_arn,
        ):
            controls.extend(page.get("Controls", []))

        return {"Controls": controls}
    except ClientError as error:
        return {
            "Error": error.response.get("Error", {}),
        }


def get_standards_controls(client, standards_response) -> list:
    standard_controls = []

    for subscription in standards_response.get(
        "StandardsSubscriptions",
        [],
    ):
        subscription_arn = subscription.get("StandardsSubscriptionArn")

        if not subscription_arn:
            continue

        controls_response = get_standard_controls(
            client,
            subscription_arn,
        )

        standard_controls.append(
            {
                "subscription": subscription,
                "controls": controls_response.get("Controls", []),
            }
        )

    return standard_controls


def get_security_hub_findings(client) -> list[dict]:
    paginator = client.get_paginator("get_findings")
    findings = []

    for page in paginator.paginate():
        findings.extend(page.get("Findings", []))

    return findings


def main() -> None:
    client = boto3.client("securityhub")

    status_response = get_security_hub_status(client)
    standards_response = get_enabled_standards(client)
    standard_controls = get_standards_controls(client, standards_response)

    print_security_hub_status(
        status_response,
        standards_response,
        standard_controls,
    )

    findings = get_security_hub_findings(client)
    path = Path("data/security_hub_findings.json")
    save_findings(findings, path)
    print(f"\nSaved {len(findings)} security findings to {path}")


if __name__ == "__main__":
    main()
