from collections import Counter
from datetime import UTC, datetime, timedelta
import json

import boto3


TARGET_EVENT_COUNT = 200
PAGE_SIZE = 50

IGNORED_EVENT_TYPES = {
    ("cloudtrail.amazonaws.com", "LookupEvents"),
    ("dynamodb.amazonaws.com", "DescribeStream"),
}


def fetch_events(days: int = 15) -> tuple[list[dict], int, int]:
    client = boto3.client("cloudtrail")
    start_time = datetime.now(UTC) - timedelta(days=days)
    paginator = client.get_paginator("lookup_events")

    events = []
    ignored_events = 0
    pages_scanned = 0

    for page in paginator.paginate(
        StartTime=start_time,
        PaginationConfig={"PageSize": PAGE_SIZE},
    ):
        pages_scanned += 1

        for event in page["Events"]:
            event_type = (
                event["EventSource"],
                event["EventName"],
            )

            if event_type in IGNORED_EVENT_TYPES:
                ignored_events += 1
                continue

            events.append(event)

            if len(events) >= TARGET_EVENT_COUNT:
                return events, ignored_events, pages_scanned

    return events, ignored_events, pages_scanned


def extract_identity(event: dict) -> tuple[str, str]:
    cloudtrail_event = json.loads(event["CloudTrailEvent"])

    identity = cloudtrail_event.get("userIdentity", {})
    identity_type = identity.get("type", "Unknown")

    if identity_type == "IAMUser":
        principal = identity.get("userName", "Unknown")

    elif identity_type == "AssumedRole":
        session_context = identity.get("sessionContext", {})
        issuer = session_context.get("sessionIssuer", {})
        principal = issuer.get("userName", "Unknown")

    elif identity_type == "AWSService":
        principal = identity.get("invokedBy", "Unknown")

    else:
        principal = (
            identity.get("arn")
            or identity.get("principalId")
            or "Unknown"
        )

    return identity_type, principal


def summarize_events(events: list[dict]) -> Counter:
    counts = Counter()

    for event in events:
        identity_type, principal = extract_identity(event)

        key = (
            identity_type,
            principal,
            event["EventSource"],
            event["EventName"],
        )

        counts[key] += 1

    return counts
