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


def print_high_priority_controls(
    prioritized_controls: pd.DataFrame,
) -> None:
    """Print controls with Critical or High findings."""
    print("High-Priority Controls")
    print("-" * 50)
    print(f"{'Control':<18} {'Total':>5}  Highest Severity")

    for control_id, row in prioritized_controls.iterrows():
        print(
            f"{control_id:<18} "
            f"{row['Total']:>5}  "
            f"{row['HighestSeverity']}"
        )


def print_resource_summary(
    resource_summary: pd.DataFrame,
    limit: int = 10,
) -> None:
    """Print the highest-priority resources."""
    print("Top Finding Resources")
    print("-" * 120)

    output = (
        resource_summary
        .head(limit)
        .reset_index()
        [["Resource", "Findings", "Controls", "HighestSeverity"]]
    )

    print(output.to_string(index=False))


def print_finding_concentration(
    concentration: pd.DataFrame,
    total_findings: int,
) -> None:
    """Print the percentage of findings concentrated in top resources."""
    print("Finding Concentration")
    print("-" * 50)
    print(f"{'Total Findings':<20}: {total_findings:,}")

    for row in concentration.itertuples(index=False):
        resource_label = "Resource" if row.Resources == 1 else "Resources"
        label = f"Top {row.Resources} {resource_label}"

        print(
            f"{label:<20}: "
            f"{row.Findings:,} ({row.Percentage:.1f}%)"
        )
