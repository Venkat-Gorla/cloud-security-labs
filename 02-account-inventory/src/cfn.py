from collections import defaultdict


def list_stacks(client) -> list[dict]:
    paginator = client.get_paginator("list_stacks")

    stacks = []

    for page in paginator.paginate(
        StackStatusFilter=[
            "CREATE_COMPLETE",
            "UPDATE_COMPLETE",
            "UPDATE_ROLLBACK_COMPLETE",
        ]
    ):
        stacks.extend(page["StackSummaries"])

    stacks.sort(key=lambda stack: stack["StackName"])

    return stacks


def list_stack_resources(client, stack_name: str) -> dict[str, list[str]]:
    paginator = client.get_paginator("list_stack_resources")

    resources: dict[str, list[str]] = defaultdict(list)

    for page in paginator.paginate(StackName=stack_name):
        for resource in page["StackResourceSummaries"]:
            resource_type = resource["ResourceType"]
            physical_id = resource.get("PhysicalResourceId", "<pending>")

            resources[resource_type].append(physical_id)

    return dict(sorted(resources.items()))
