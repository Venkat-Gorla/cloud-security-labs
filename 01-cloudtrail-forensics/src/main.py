"""
uv run src/main.py --user <username>
uv run src/main.py --user <username> --days 3
"""
import argparse
from collections import Counter
from cloudtrail import extract_identity, fetch_human_events

NUMBER_OF_DAYS = 3

REPORT_EXCLUDED_EVENTS = {
    ("cloudtrail.amazonaws.com", "LookupEvents"),
}


def summarize_events(events: list[dict]) -> Counter:
    summary = Counter()

    for event in events:
        event_key = (event["EventSource"], event["EventName"])
        if event_key in REPORT_EXCLUDED_EVENTS:
            continue

        summary[
            (
                extract_identity(event),
                event["EventSource"],
                event["EventName"],
            )
        ] += 1

    return summary


def print_report(events: list[dict], days: int) -> None:
    summary = summarize_events(events)

    print("CloudTrail IAMUser Activity Summary")
    print("=" * 100)
    print(f"Period          : Last {days} days")
    print(f"Events Fetched  : {len(events)}")
    print(f"Activities      : {len(summary)}")
    print("=" * 100)
    print()

    print(
        f"{'Count':>8}  "
        f"{'User':<20} "
        f"{'Service':<35} "
        f"{'Event'}"
    )
    print("-" * 100)

    for (
        user,
        service,
        event_name,
    ), count in summary.most_common():

        print(
            f"{count:>8}  "
            f"{user:<20} "
            f"{service:<35} "
            f"{event_name}"
        )


def parse_args():
    parser = argparse.ArgumentParser(
        description="CloudTrail IAMUser Activity Summary"
    )
    parser.add_argument("--user", required=True, help="Username to analyze")
    parser.add_argument(
        "--days",
        type=int,
        default=NUMBER_OF_DAYS,
        help="Number of days to analyze")

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    events, total_scanned = fetch_human_events(
        username=args.user,
        days=args.days
    )

    print_report(events, args.days)


if __name__ == "__main__":
    main()
