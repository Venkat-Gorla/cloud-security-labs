from collections import Counter
from datetime import UTC, datetime, timedelta

import boto3


TARGET_EVENT_COUNT = 100
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


def summarize_events(events: list[dict]) -> Counter:
    counts = Counter()

    for event in events:
        username = event.get("Username", "Unknown")

        key = (
            username,
            event["EventSource"],
            event["EventName"],
        )

        counts[key] += 1

    return counts
