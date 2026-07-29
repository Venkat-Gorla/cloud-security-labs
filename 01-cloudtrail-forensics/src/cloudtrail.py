from collections import Counter
from datetime import UTC, datetime, timedelta

import boto3


MAX_PAGES = 5
PAGE_SIZE = 50


def fetch_events(days: int = 15) -> list[dict]:
    cloudtrail_client = boto3.client("cloudtrail")
    paginator = cloudtrail_client.get_paginator("lookup_events")
    start_time = datetime.now(UTC) - timedelta(days=days)

    events = []

    for page_number, page in enumerate(
        paginator.paginate(
            StartTime=start_time,
            PaginationConfig={"PageSize": PAGE_SIZE},
        ),
        start=1,
    ):
        for event in page["Events"]:
            if (
                event["EventSource"] == "cloudtrail.amazonaws.com"
                and event["EventName"] == "LookupEvents"
            ):
                continue

            events.append(event)

        if page_number >= MAX_PAGES:
            break

    return events


def summarize_events(events: list[dict]) -> Counter:
    counts = Counter()

    for event in events:
        key = (
            event["Username"] if "Username" in event else "Unknown",
            event["EventSource"],
            event["EventName"],
        )

        counts[key] += 1

    return counts
