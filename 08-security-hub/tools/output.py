"""Formatting and presentation helpers for the lab tools."""

from datetime import datetime

SEPARATOR = "=" * 50
SUBSEPARATOR = "-" * 50


def get_hub_status(response: dict) -> str:
    return "ENABLED" if response.get("HubArn") else "DISABLED"


def format_timestamp(value: str) -> str:
    if not value:
        return "-"

    timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def format_standard_name(standards_arn: str) -> str:
    if "cis-aws-foundations-benchmark" in standards_arn:
        return "CIS AWS Foundations Benchmark v1.2.0"

    if "aws-foundational-security-best-practices" in standards_arn:
        return "AWS Foundational Security Best Practices v1.0.0"

    return standards_arn


def print_hub_status(status: dict) -> None:
    hub_arn = status.get("HubArn", "-")
    region = hub_arn.split(":")[3] if hub_arn != "-" else "-"

    print("AWS Security Hub")
    print(SEPARATOR)
    print()
    print(f"Status              : {get_hub_status(status)}")
    print(f"Region              : {region}")
    print(
        f"Subscribed At       : "
        f"{format_timestamp(status.get('SubscribedAt', ''))}"
    )
    print(
        f"Auto-enable Controls: "
        f"{status.get('AutoEnableControls', '-')}"
    )
    print(
        f"Finding Generator   : "
        f"{status.get('ControlFindingGenerator', '-')}"
    )
    print()


def print_enabled_standards(standards_response: dict) -> None:
    print("Standards")
    print(SUBSEPARATOR)

    subscriptions = standards_response.get("StandardsSubscriptions", [])

    for subscription in subscriptions:
        name = format_standard_name(
            subscription.get("StandardsArn", "-")
        )
        status = subscription.get("StandardsStatus", "-")

        print(name)
        print(f"Status              : {status}")
        print()


def print_security_hub_status(
    status: dict,
    standards_response: dict,
) -> None:
    print_hub_status(status)
    print_enabled_standards(standards_response)
