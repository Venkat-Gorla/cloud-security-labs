"""
uv run src/summary.py
"""

import boto3
from collections import Counter
from cfn import list_stack_resources, list_stacks


def print_account_summary(stacks, resource_types) -> None:
    print("AWS Account Summary")
    print("=" * 100)
    print()

    print(f"CloudFormation Stacks : {len(stacks)}")
    print(f"Managed Resources     : {sum(resource_types.values())}")
    print(f"Resource Types        : {len(resource_types)}")
    print()


def print_resources_by_type(resource_types) -> None:
    print("=" * 100)
    print("Resources by Type")
    print("=" * 100)
    print()

    print(f"{'Count':>8}  Resource Type")
    print("-" * 100)

    for resource_type, count in resource_types.most_common():
        print(f"{count:>8}  {resource_type}")


def print_largest_stacks(stack_sizes) -> None:
    print()
    print("=" * 100)
    print("Largest Stacks")
    print("=" * 100)
    print()

    print(f"{'Resources':>10}  Stack")
    print("-" * 100)

    for stack_name, count in sorted(stack_sizes, key=lambda x: x[1], reverse=True):
        print(f"{count:>10}  {stack_name}")


def main() -> None:
    client = boto3.client("cloudformation")
    stacks = list_stacks(client)

    resource_types = Counter()
    stack_sizes = []

    for stack in stacks:
        resources = list_stack_resources(client, stack["StackName"])
        resource_count = 0

        for resource_type, physical_ids in resources.items():
            count = len(physical_ids)
            resource_types[resource_type] += count
            resource_count += count

        stack_sizes.append((stack["StackName"], resource_count))

    print_account_summary(stacks, resource_types)
    print_resources_by_type(resource_types)
    print_largest_stacks(stack_sizes)


if __name__ == "__main__":
    main()
