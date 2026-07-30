"""
uv run src/unmanaged.py
"""

import boto3

from cfn import get_managed_resource_names
from services.lambda_service import get_function_names
from services.dynamodb_service import get_table_names


def print_unmanaged_resources(
    resource_name: str,
    managed_resources: set[str],
    all_resources: set[str],
) -> None:
    unmanaged_resources = sorted(all_resources - managed_resources)

    print(f"{resource_name} Outside CloudFormation")
    print("=" * 100)
    print()

    print(f"CloudFormation : {len(managed_resources)}")
    print(f"Total          : {len(all_resources)}")
    print(f"Outside CF     : {len(unmanaged_resources)}")
    print()

    if not unmanaged_resources:
        print(f"No {resource_name.lower()} found outside CloudFormation.")
        return

    print("-" * 100)

    for resource in unmanaged_resources:
        print(resource)


def handle_unmanaged_lambda(cloudformation_client) -> None:
    lambda_client = boto3.client("lambda")

    managed_functions = get_managed_resource_names(
        cloudformation_client,
        "AWS::Lambda::Function",
    )

    all_functions = get_function_names(lambda_client)

    print_unmanaged_resources(
        "Lambda Functions",
        managed_functions,
        all_functions,
    )


def handle_unmanaged_dynamodb(cloudformation_client) -> None:
    dynamodb_client = boto3.client("dynamodb")

    managed_tables = get_managed_resource_names(
        cloudformation_client,
        "AWS::DynamoDB::Table",
    )
    all_tables = get_table_names(dynamodb_client)

    print_unmanaged_resources(
        "DynamoDB Tables",
        managed_tables,
        all_tables,
    )


def main() -> None:
    cloudformation_client = boto3.client("cloudformation")

    handle_unmanaged_lambda(cloudformation_client)
    print()
    handle_unmanaged_dynamodb(cloudformation_client)


if __name__ == "__main__":
    main()
