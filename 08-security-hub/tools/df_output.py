"""Output helpers for Pandas DataFrames."""

import pandas as pd


def print_nested_field_types(findings_df: pd.DataFrame) -> None:
    """Print the Python types used by nested finding fields."""
    fields = [
        "Compliance",
        "Severity",
        "Resources",
        "Remediation",
        "ProductFields",
        "FindingProviderFields",
    ]

    print("Nested Field Types")
    print("-" * 50)

    for field in fields:
        types = findings_df[field].map(type).value_counts()

        print(f"{field}:")
        for value_type, count in types.items():
            print(f"  {value_type.__name__}: {count}")


def print_findings_summary(findings_df: pd.DataFrame) -> None:
    """Print the Security Hub findings summary."""
    print("Security Hub Findings Analysis")
    print("=" * 50)
    print()
    print(f"Findings: {len(findings_df)}")
    print(f"Columns : {len(findings_df.columns)}")
    print()


def print_severity_summary(severity_summary: pd.Series) -> None:
    """Print findings grouped by severity."""
    print("Findings by Severity")
    print("-" * 50)

    for severity, count in severity_summary.items():
        print(f"{severity:<18}: {count}")


def print_control_summary(
    control_summary: pd.Series,
    limit: int = 10,
) -> None:
    """Print the highest-volume Security Hub controls."""
    print("Top Findings by Control")
    print("-" * 50)

    for control_id, count in control_summary.head(limit).items():
        print(f"{control_id:<18}: {count}")


def print_resource_type_summary(
    resource_type_summary: pd.Series,
    limit: int = 10,
) -> None:
    """Print the highest-volume AWS resource types."""
    print("Top Findings by Resource Type")
    print("-" * 50)

    for resource_type, count in resource_type_summary.head(limit).items():
        print(f"{resource_type:<24}: {count}")
