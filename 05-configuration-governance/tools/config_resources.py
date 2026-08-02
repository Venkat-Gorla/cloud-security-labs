"""
uv run tools/config_resources.py
"""

import boto3

RESOURCE_TYPES = {
    "AWS::Lambda::Function": "Lambda Functions",
    "AWS::DynamoDB::Table": "DynamoDB Tables",
    # "AWS::S3::Bucket": "S3 Buckets",
    "AWS::CloudFormation::Stack": "CloudFormation Stacks",
}


def list_resources(
    client,
    resource_type: str,
) -> list[str]:
    resources: list[str] = []
    paginator = client.get_paginator("list_discovered_resources")

    for page in paginator.paginate(resourceType=resource_type):
        resources.extend(page["resourceIdentifiers"])

    return sorted(
        resource["resourceName"]
        for resource in resources
    )


def print_resources(
    heading: str,
    resources: list[str],
) -> None:
    print(f"{heading} ({len(resources)})")
    print("-" * 100)

    if not resources:
        print("None")
    else:
        for resource in resources:
            print(resource)

    print()


def main() -> None:
    client = boto3.client("config")

    print("AWS Config Resources")
    print("=" * 100)
    print()

    for resource_type, heading in RESOURCE_TYPES.items():
        resources = list_resources(client, resource_type,)
        print_resources(heading, resources,)


if __name__ == "__main__":
    main()
