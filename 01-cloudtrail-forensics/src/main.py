"""
uv run src/main.py
"""
from cloudtrail import fetch_events, summarize_events


def main() -> None:
    events, excluded_events, pages_scanned = fetch_events()
    summary = summarize_events(events)

    print()
    print("CloudTrail Activity Summary")
    print("=" * 120)
    print("Period            : Last 15 days")
    print(f"Events Analyzed   : {len(events)}")
    print(f"Events Excluded   : {excluded_events}")
    print(f"Pages Scanned     : {pages_scanned}")
    print(f"Unique Activities : {len(summary)}")
    print("=" * 120)
    print()

    print(
        f"{'Count':>8}  "
        f"{'Identity Type':<18} "
        f"{'Principal':<35} "
        f"{'Service':<35} "
        f"{'Event'}"
    )
    print("-" * 120)

    for (
        identity_type,
        principal,
        service,
        event,
    ), count in summary.most_common():
        print(
            f"{count:>8}  "
            f"{identity_type:<18} "
            f"{principal:<35} "
            f"{service:<35} "
            f"{event}"
        )


if __name__ == "__main__":
    main()
