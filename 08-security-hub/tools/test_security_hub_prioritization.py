"""
uv run tools/test_security_hub_prioritization.py
"""

import pandas as pd
from security_hub_prioritization import (
    SEVERITY_RANK,
    add_severity_priority,
)


def print_test_header(name: str) -> None:
    """Print a header for a manual validation test."""
    print()
    print(f"Test: {name}")
    print("-" * 40)


def test_add_severity_priority() -> None:
    """Validate highest severity and severity ranking."""
    print_test_header("add_severity_priority")

    summary = pd.DataFrame(
        {
            "CRITICAL": [1, 0, 0],
            "HIGH": [0, 1, 0],
            "MEDIUM": [0, 0, 2],
            "LOW": [0, 0, 1],
            "INFORMATIONAL": [15, 15, 5],
        },
        index=["S3.2", "S3.8", "S3.9"],
    )

    result = add_severity_priority(summary)

    assert result.loc["S3.2", "HighestSeverity"] == "CRITICAL"
    assert result.loc["S3.8", "HighestSeverity"] == "HIGH"
    assert result.loc["S3.9", "HighestSeverity"] == "MEDIUM"

    assert (
        result["SeverityRank"]
        == result["HighestSeverity"].map(SEVERITY_RANK)
    ).all()

    print("✓ S3.2 → CRITICAL")
    print("✓ S3.8 → HIGH")
    print("✓ S3.9 → MEDIUM")
    print("✓ Severity ranks match SEVERITY_RANK")
    print()
    print(result)


if __name__ == "__main__":
    test_add_severity_priority()
