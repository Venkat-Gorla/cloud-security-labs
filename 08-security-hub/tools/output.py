"""Formatting and presentation helpers for the lab tools."""

from datetime import datetime

SEPARATOR = "=" * 50
SUBSEPARATOR = "-" * 50

STANDARD_NAMES = {
    "cis-aws-foundations-benchmark": "CIS AWS Foundations Benchmark",
    "aws-foundational-security-best-practices": (
        "AWS Foundational Security Best Practices"
    ),
}


def get_hub_status(response: dict) -> str:
    return "ENABLED" if response.get("HubArn") else "DISABLED"


def format_timestamp(value: str) -> str:
    if not value:
        return "-"

    timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def format_standard(standards_arn: str) -> tuple[str, str]:
    parts = standards_arn.rstrip("/").split("/")

    for identifier, name in STANDARD_NAMES.items():
        if identifier in parts:
            index = parts.index(identifier)
            version = parts[index + 2] if len(parts) > index + 2 else "-"
            return name, version

    return standards_arn, "-"


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
        name, version = format_standard(
            subscription.get("StandardsArn", "-")
        )

        status = subscription.get("StandardsStatus", "-")

        print(name)
        print(f"Version             : {version}")
        print(f"Status              : {status}")
        print()


def get_control_summary(controls: list[dict]) -> tuple[int, int]:
    total = len(controls)
    enabled = sum(
        1
        for control in controls
        if control.get("ControlStatus") == "ENABLED"
    )

    return total, enabled


def print_control_summary(
    subscription: dict,
    controls: list[dict],
) -> None:
    name, version = format_standard(
        subscription.get("StandardsArn", "-")
    )
    total, enabled = get_control_summary(controls)

    print(name)
    print(f"Version             : {version}")
    print(f"Controls            : {total}")
    print(f"Enabled             : {enabled}")
    print()


def print_control_summaries(
    standard_controls: list[dict],
) -> None:
    print("Security Controls")
    print(SUBSEPARATOR)

    for standard in standard_controls:
        print_control_summary(
            standard["subscription"],
            standard["controls"],
        )


def print_security_hub_status(
    status: dict,
    standards_response: dict,
    standard_controls: list[dict],
) -> None:
    print_hub_status(status)
    print_enabled_standards(standards_response)
    print_control_summaries(standard_controls)
