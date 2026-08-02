import json


def print_common(item: dict) -> None:
    print("Configuration Item")
    print("=" * 100)
    print()

    print(f"Resource Type       : {item['resourceType']}")
    print(f"Resource Name       : {item['resourceName']}")
    print(f"Resource ID         : {item['resourceId']}")
    print(f"Region              : {item['awsRegion']}")
    print(
        f"Capture Time        : "
        f"{item['configurationItemCaptureTime']}"
    )
    print(
        f"Resource Created    : "
        f"{item['resourceCreationTime']}"
    )
    print(
        f"Status              : "
        f"{item['configurationItemStatus']}"
    )
    print(
        f"Relationships       : "
        f"{len(item['relationships'])}"
    )
    print()


def print_dynamodb(configuration: dict) -> None:
    print("DynamoDB Table")
    print("-" * 100)

    print(
        f"Billing Mode        : "
        f"{configuration['billingModeSummary']['billingMode']}"
    )
    print(
        f"Table Status        : "
        f"{configuration['tableStatus']}"
    )
    print(
        f"Deletion Protection : "
        f"{configuration['deletionProtectionEnabled']}"
    )


def print_unknown(configuration: dict) -> None:
    print("Configuration Keys")
    print("-" * 100)

    for key in sorted(configuration.keys()):
        print(key)

    print()


def print_configuration_item(item: dict) -> None:
    print_common(item)

    configuration = json.loads(item["configuration"])

    match item["resourceType"]:
        case "AWS::DynamoDB::Table":
            print_dynamodb(configuration)

        case _:
            print_unknown(configuration)
