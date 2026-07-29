"""
uv run src/main.py
"""
from cloudtrail import fetch_events, summarize_events


def main() -> None:
    events, ignored_events, pages_scanned = fetch_events()
    summary = summarize_events(events)

    print()
    print("CloudTrail Activity Summary")
    print("=" * 100)
    print("Period            : Last 15 days")
    print(f"Events Analyzed   : {len(events)}")
    print(f"Events Ignored    : {ignored_events}")
    print(f"Pages Scanned     : {pages_scanned}")
    print(f"Unique Activities : {len(summary)}")
    print("=" * 100)
    print()

    print(f"{'Count':>8}  {'User':<35} {'Service':<35} {'Event'}")
    print("-" * 100)

    for (user, service, event), count in summary.most_common():
        print(f"{count:>8}  {user:<35} {service:<35} {event}")


if __name__ == "__main__":
    main()
