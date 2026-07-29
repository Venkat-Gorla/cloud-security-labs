from collections import Counter
from datetime import UTC, datetime, timedelta
import json

import boto3


TARGET_EVENT_COUNT = 200
PAGE_SIZE = 50

EXCLUDED_EVENT_TYPES = {
    # Tool querying itself
    ("cloudtrail.amazonaws.com", "LookupEvents"),

    # DynamoDB stream polling noise from Lambda integrations
    ("dynamodb.amazonaws.com", "DescribeStream"),

    # AWS Resource Explorer inventory/discovery noise
    ("resource-explorer-2.amazonaws.com", "Search"),
    ("resource-explorer-2.amazonaws.com", "ListIndexes"),
    ("resource-explorer-2.amazonaws.com", "ListSupportedResourceTypes"),

    # Common AWS discovery APIs
    ("ec2.amazonaws.com", "DescribeRegions"),
    ("ec2.amazonaws.com", "DescribeAvailabilityZones"),

    # Resource Explorer backend discovery
    ("cloudcontrolapi.amazonaws.com", "GetResource"),
    ("cloudcontrolapi.amazonaws.com", "ListResources"),

    # Read-only discovery APIs
    ("apigateway.amazonaws.com", "GetRestApis"),
    ("apigateway.amazonaws.com", "GetStages"),
    ("apigateway.amazonaws.com", "GetStage"),

    # Certificate/config discovery
    ("acm.amazonaws.com", "ListCertificates"),
    ("ssm.amazonaws.com", "DescribeParameters"),
}


def fetch_events(days: int = 15) -> tuple[list[dict], int, int]:
    client = boto3.client("cloudtrail")
    start_time = datetime.now(UTC) - timedelta(days=days)
    paginator = client.get_paginator("lookup_events")

    events = []
    excluded_events = 0
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

            if event_type in EXCLUDED_EVENT_TYPES:
                excluded_events += 1
                continue

            events.append(event)

            if len(events) >= TARGET_EVENT_COUNT:
                return events, excluded_events, pages_scanned

    return events, excluded_events, pages_scanned


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


def filter_human_events(events: list[dict]) -> list[dict]:
    return [
        event
        for event in events
        if extract_identity(event)[0] == "IAMUser"
    ]


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
