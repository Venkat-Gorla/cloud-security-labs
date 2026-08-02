"""
uv run tools/config_recorder.py
"""

import boto3


def print_recording_strategy(recording_group: dict) -> None:
    print("Recording Strategy")

    strategy = recording_group["recordingStrategy"]["useOnly"]
    if strategy == "EXCLUSION_BY_RESOURCE_TYPES":
        excluded = recording_group["exclusionByResourceTypes"]["resourceTypes"]

        print("Mode              : Exclude resource types")
        print(f"Excluded Types    : {len(excluded)}")

        for resource_type in sorted(excluded):
            print(f"    {resource_type}")
    else:
        print(f"Mode              : {strategy}")

    print()
    print(
        f"Global Resource Types : "
        f"{recording_group['includeGlobalResourceTypes']}"
    )


def print_recorder(recorder: dict) -> None:
    print("Configuration Recorder")
    print("=" * 100)
    print()

    role_name = recorder["roleARN"].split("/")[-1]
    print(f"Name              : {recorder['name']}")
    print(f"Role Name         : {role_name}\n")

    recording_group = recorder["recordingGroup"]
    print_recording_strategy(recording_group)


def print_status(status: dict) -> None:
    print()
    print("Recorder Status")
    print("=" * 100)
    print()

    print(f"Recording         : {status['recording']}")
    print(f"Last Start Time   : {status.get('lastStartTime', '-')}")
    print(f"Last Stop Time    : {status.get('lastStopTime', '-')}")
    print(f"Last Status       : {status.get('lastStatus', '-')}")
    print(f"Last Error Code   : {status.get('lastErrorCode', '-')}")
    print(f"Last Error Msg    : {status.get('lastErrorMessage', '-')}")


def main() -> None:
    client = boto3.client("config")
    recorders = client.describe_configuration_recorders()[
        "ConfigurationRecorders"
    ]

    if not recorders:
        print("AWS Config is not configured.")
        return

    statuses = client.describe_configuration_recorder_status()[
        "ConfigurationRecordersStatus"
    ]

    print_recorder(recorders[0])

    if statuses:
        print_status(statuses[0])


if __name__ == "__main__":
    main()
