"""
uv run src/inventory.py
"""
import boto3
from cfn import list_stacks, list_stack_resources


def print_stack_header(stack: dict) -> None:
    print("-" * 100)
    print(stack["StackName"])
    print("-" * 100)
    print()

    print(f"Status     : {stack['StackStatus']}")
    print(f"Created    : {stack['CreationTime']:%Y-%m-%d %H:%M}")
    print(
        f"Updated    : "
        f"{stack.get('LastUpdatedTime', '-')}"
    )


def print_stack_resources(resources: dict[str, list[str]]) -> None:
    resource_count = sum(len(items) for items in resources.values())

    print(f"Resources  : {resource_count}")
    print()

    for resource_type, physical_ids in resources.items():
        print(resource_type)

        for physical_id in sorted(physical_ids):
            print(f"    {physical_id}")

        print()


def main() -> None:
    client = boto3.client("cloudformation")

    print("AWS Account Inventory")
    print("=" * 100)
    print()

    stacks = list_stacks(client)

    print(f"Stacks Found : {len(stacks)}")
    print()

    for stack in stacks:
        print_stack_header(stack)
        resources = list_stack_resources(client, stack["StackName"])
        print_stack_resources(resources)

    print("=" * 100)


if __name__ == "__main__":
    main()
