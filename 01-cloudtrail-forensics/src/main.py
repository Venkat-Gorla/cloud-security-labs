"""
uv run src/main.py
"""
from collections import Counter
from cloudtrail import extract_identity, fetch_human_events


def summarize_events(events: list[dict]) -> Counter:
    summary = Counter()

    for event in events:
        summary[
            (
                extract_identity(event),
                event["EventSource"],
                event["EventName"],
            )
        ] += 1

    return summary


def print_report(events: list[dict], total_scanned: int) -> None:
    summary = summarize_events(events)

    print("CloudTrail Human Activity Summary")
    print("=" * 100)
    print("Period          : Last 15 days")
    print(f"Events Scanned  : {total_scanned}")
    print(f"Human Events    : {len(events)}")
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


def main() -> None:
    events, total_scanned = fetch_human_events()

    print_report(
        events,
        total_scanned,
    )


if __name__ == "__main__":
    main()
