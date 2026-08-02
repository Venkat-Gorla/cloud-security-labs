"""
uv run tools/config_resource.py AWS::DynamoDB::Table tinyurl-mappings
"""

import sys
import boto3
from config_formatter import print_configuration_item


def get_latest_configuration_item(
    client,
    resource_type: str,
    resource_name: str,
) -> dict | None:
    response = client.get_resource_config_history(
        resourceType=resource_type,
        resourceId=resource_name,
        limit=1,
    )

    history = response["configurationItems"]

    if not history:
        return None

    return history[0]


def main() -> None:
    if len(sys.argv) != 3:
        print(
            "Usage:\n"
            "uv run tools/config_resource.py "
            "<resource-type> <resource-name>"
        )
        raise SystemExit(1)

    resource_type = sys.argv[1]
    resource_name = sys.argv[2]

    client = boto3.client("config")

    item = get_latest_configuration_item(
        client,
        resource_type,
        resource_name,
    )

    if item is None:
        print("Configuration item not found.")
        return

    print_configuration_item(item)


if __name__ == "__main__":
    main()
