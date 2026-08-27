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
