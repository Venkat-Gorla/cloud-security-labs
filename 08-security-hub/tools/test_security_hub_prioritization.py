"""
uv run tools/test_security_hub_prioritization.py
"""

import pandas as pd

from security_hub_prioritization import (
    SEVERITY_RANK,
    add_severity_priority,
    prioritize_controls,
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


def test_prioritize_controls() -> None:
    """Validate control ordering by severity and finding volume."""
    print_test_header("prioritize_controls")

    summary = pd.DataFrame(
        {
            "CRITICAL": [0, 1, 1, 0],
            "HIGH": [0, 0, 0, 1],
            "MEDIUM": [2, 0, 0, 0],
            "LOW": [0, 0, 0, 0],
            "INFORMATIONAL": [5, 0, 5, 15],
        },
        index=["S3.9", "S3.2", "IAM.6", "S3.8"],
    )

    summary["Total"] = summary.sum(axis=1)
    original_summary = summary.copy()

    result = prioritize_controls(summary)

    expected_order = [
        "IAM.6",
        "S3.2",
        "S3.8",
        "S3.9",
    ]

    assert result.index.tolist() == expected_order

    assert result["HighestSeverity"].tolist() == [
        "CRITICAL",
        "CRITICAL",
        "HIGH",
        "MEDIUM",
    ]

    assert result["Total"].tolist() == [6, 1, 16, 7]
    assert summary.equals(original_summary)
    assert "SeverityRank" not in result.columns

    print("✓ CRITICAL controls appear first")
    print("✓ HIGH controls appear before MEDIUM controls")
    print("✓ Finding volume breaks severity ties")
    print("✓ Original DataFrame remains unchanged")
    print("✓ SeverityRank is removed from the returned result")
    print()
    print(result[["Total", "HighestSeverity"]])


def main() -> None:
    test_add_severity_priority()
    test_prioritize_controls()
    print()
    print("All prioritization tests passed.")


if __name__ == "__main__":
    main()
