"""
uv run tools/config_metrics.py
"""

from datetime import UTC, datetime, timedelta
import boto3

RESOURCE_TYPES = [
    "All",
    "AWS::Lambda::Function",
    "AWS::DynamoDB::Table",
    "AWS::S3::Bucket",
    "AWS::CloudFormation::Stack",
]


def get_configuration_items_recorded(
    client,
    resource_type: str,
) -> int:
    days = 1

    response = client.get_metric_statistics(
        Namespace="AWS/Config",
        MetricName="ConfigurationItemsRecorded",
        Dimensions=[
            {
                "Name": "ResourceType",
                "Value": resource_type,
            }
        ],
        StartTime=datetime.now(UTC) - timedelta(days=days),
        EndTime=datetime.now(UTC),
        Period=days * 24 * 60 * 60,
        Statistics=["Sum"],
    )

    datapoints = response["Datapoints"]

    if not datapoints:
        return 0

    return int(datapoints[0]["Sum"])


def main() -> None:
    client = boto3.client("cloudwatch")

    print("Configuration Item Metrics")
    print("=" * 100)
    print()

    for resource_type in RESOURCE_TYPES:
        count = get_configuration_items_recorded(
            client,
            resource_type,
        )

        print(f"{resource_type:<35} {count:>8}")


if __name__ == "__main__":
    main()
