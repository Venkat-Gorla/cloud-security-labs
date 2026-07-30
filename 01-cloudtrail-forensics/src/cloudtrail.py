from datetime import UTC, datetime, timedelta
import json
import boto3


PAGE_SIZE = 50
PROGRESS_INTERVAL = 40


def fetch_human_events(username: str, days: int) -> tuple[list[dict], int]:
    client = boto3.client("cloudtrail")
    start_time = datetime.now(UTC) - timedelta(days=days)
    paginator = client.get_paginator("lookup_events")

    human_events = []
    pages_processed = 0
    total_events_scanned = 0

    print("Scanning CloudTrail history...\n")

    for page in paginator.paginate(
        StartTime=start_time,
        LookupAttributes=[
            {
            "AttributeKey": "Username",
            "AttributeValue": username,
            }
        ],
        PaginationConfig={"PageSize": PAGE_SIZE},
    ):
        pages_processed += 1

        for event in page["Events"]:
            total_events_scanned += 1

            if is_human_event(event):
                human_events.append(event)

        if pages_processed % PROGRESS_INTERVAL == 0:
            print(
                f"Pages processed: {pages_processed} | "
                f"Events fetched: {total_events_scanned}"
            )

    print("\nCloudTrail scan complete.\n")

    return human_events, total_events_scanned


def is_human_event(event: dict) -> bool:
    cloudtrail_event = json.loads(event["CloudTrailEvent"])
    identity = cloudtrail_event.get("userIdentity", {})

    return identity.get("type") == "IAMUser"


def extract_identity(event: dict) -> str:
    cloudtrail_event = json.loads(event["CloudTrailEvent"])
    identity = cloudtrail_event.get("userIdentity", {})

    return identity.get("userName", "Unknown")


def classify_origin(event: dict) -> str:
    cloudtrail_event = json.loads(event["CloudTrailEvent"])
    user_agent = cloudtrail_event.get("userAgent", "").lower()

    if "aws-cli" in user_agent:
        return "AWS CLI"

    if "boto3" in user_agent or "botocore" in user_agent:
        return "Python SDK"

    if "console.amazonaws.com" in user_agent:
        return "Console"

    if (
        "mozilla/" in user_agent
        and "chrome/" in user_agent
    ):
        return "Console Browser"

    if "cloudformation" in user_agent:
        return "CloudFormation"

    if "internal" in user_agent:
        return "AWS Internal"

    return "Unknown"
