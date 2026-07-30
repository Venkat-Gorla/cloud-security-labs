"""
uv run src/unmanaged.py
"""

import boto3

from cfn import get_managed_resource_names
from services.lambda_service import get_function_names


def print_unmanaged_lambda(
    managed_resources: set[str],
    all_resources: set[str],
) -> None:
    unmanaged_resources = sorted(all_resources - managed_resources)

    print("Unmanaged Lambda Functions")
    print("=" * 100)
    print()

    print(f"Managed Functions   : {len(managed_resources)}")
    print(f"Total Functions     : {len(all_resources)}")
    print(f"Unmanaged Functions : {len(unmanaged_resources)}")
    print()

    if not unmanaged_resources:
        print("No unmanaged Lambda functions found.")
        return

    print("-" * 100)

    for function_name in unmanaged_resources:
        print(function_name)


def main() -> None:
    cloudformation_client = boto3.client("cloudformation")
    lambda_client = boto3.client("lambda")

    managed_functions = get_managed_resource_names(
        cloudformation_client,
        "AWS::Lambda::Function",
    )

    all_functions = get_function_names(lambda_client)

    print_unmanaged_lambda(
        managed_functions,
        all_functions,
    )


if __name__ == "__main__":
    main()
