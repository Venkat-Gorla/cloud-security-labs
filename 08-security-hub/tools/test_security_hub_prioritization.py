"""
uv run tools/test_security_hub_prioritization.py
"""

import pandas as pd

from security_hub_prioritization import (
    SEVERITY_RANK,
    add_severity_priority,
    prioritize_controls,
    summarize_findings_by_resource,
    summarize_finding_concentration,
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


def test_summarize_findings_by_resource() -> None:
    """Validate finding volume, control diversity, and severity by resource."""
    print_test_header("summarize_findings_by_resource")

    findings_df = pd.DataFrame(
        {
            "Resource": [
                "bucket-a",
                "bucket-a",
                "bucket-a",
                "role-a",
            ],
            "ControlId": [
                "S3.2",
                "S3.8",
                "S3.2",
                "IAM.6",
            ],
            "Severity": [
                "CRITICAL",
                "HIGH",
                "INFORMATIONAL",
                "MEDIUM",
            ],
        }
    )

    result = summarize_findings_by_resource(findings_df)

    assert result.loc["bucket-a", "Findings"] == 3
    assert result.loc["bucket-a", "Controls"] == 2
    assert result.loc["bucket-a", "CRITICAL"] == 1
    assert result.loc["bucket-a", "HIGH"] == 1
    assert result.loc["bucket-a", "INFORMATIONAL"] == 1
    assert result.loc["bucket-a", "HighestSeverity"] == "CRITICAL"

    assert result.loc["role-a", "Findings"] == 1
    assert result.loc["role-a", "Controls"] == 1
    assert result.loc["role-a", "MEDIUM"] == 1
    assert result.loc["role-a", "HighestSeverity"] == "MEDIUM"

    assert result.index.tolist() == ["bucket-a", "role-a"]

    print("✓ bucket-a → 3 findings")
    print("✓ bucket-a → 2 distinct controls")
    print("✓ bucket-a → CRITICAL is highest severity")
    print("✓ role-a → 1 finding")
    print("✓ role-a → 1 distinct control")
    print("✓ role-a → MEDIUM is highest severity")
    print()
    print(
        result[
            [
                "Findings",
                "Controls",
                "CRITICAL",
                "HIGH",
                "MEDIUM",
                "INFORMATIONAL",
                "HighestSeverity",
            ]
        ]
    )


def test_summarize_finding_concentration() -> None:
    """Validate cumulative finding concentration by top resources."""
    print_test_header("summarize_finding_concentration")

    resource_summary = pd.DataFrame(
        {
            "Findings": [10, 5, 3, 2],
            "Controls": [8, 5, 3, 2],
        },
        index=[
            "resource-a",
            "resource-b",
            "resource-c",
            "resource-d",
        ],
    )

    result = summarize_finding_concentration(
        resource_summary,
        [1, 2, 3],
    )

    assert result["Resources"].tolist() == [1, 2, 3]
    assert result["Findings"].tolist() == [10, 15, 18]

    assert result["Percentage"].tolist() == [
        50.0,
        75.0,
        90.0,
    ]

    print("✓ Top 1 resource → 10 findings → 50.0%")
    print("✓ Top 2 resources → 15 findings → 75.0%")
    print("✓ Top 3 resources → 18 findings → 90.0%")
    print()
    print(result)


def main() -> None:
    test_add_severity_priority()
    test_prioritize_controls()
    test_summarize_findings_by_resource()
    test_summarize_finding_concentration()
    print()
    print("=" * 40)
    print("✓✓ All prioritization tests passed.")
    print("=" * 40)


if __name__ == "__main__":
    main()
