"""
Security Hub finding prioritization.

vegorla: consider unit tests for these functions
"""

import pandas as pd


SEVERITY_ORDER = [
    "CRITICAL",
    "HIGH",
    "MEDIUM",
    "LOW",
    "INFORMATIONAL",
]

SEVERITY_RANK = {
    severity: rank
    for rank, severity in enumerate(SEVERITY_ORDER)
}
SEVERITY_RANK["UNKNOWN"] = len(SEVERITY_ORDER)


def get_highest_severity(
    row: pd.Series,
    severity_order: list[str] = SEVERITY_ORDER,
) -> str:
    """Return the highest severity present in a finding summary row."""
    for severity in severity_order:
        if row[severity] > 0:
            return severity

    return "UNKNOWN"


def prioritize_controls(
    summary: pd.DataFrame,
) -> pd.DataFrame:
    """Rank controls by highest severity and finding volume."""
    result = summary.copy()

    result["HighestSeverity"] = result.apply(
        get_highest_severity,
        axis=1,
    )

    result["SeverityRank"] = result["HighestSeverity"].map(
        SEVERITY_RANK
    )

    return (
        result
        .sort_values(
            ["SeverityRank", "Total"],
            ascending=[True, False],
        )
        .drop(columns="SeverityRank")
    )


def find_high_priority_controls(
    findings_df: pd.DataFrame,
) -> pd.DataFrame:
    """Return controls with Critical or High findings."""
    control_severity = (
        findings_df
        .groupby(["ControlId", "Severity"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=SEVERITY_ORDER, fill_value=0)
    )

    control_severity["Total"] = control_severity.sum(axis=1)

    prioritized_controls = prioritize_controls(control_severity)

    return prioritized_controls[
        prioritized_controls["HighestSeverity"].isin(
            ["CRITICAL", "HIGH"]
        )
    ]


def summarize_findings_by_resource(
    findings_df: pd.DataFrame,
) -> pd.DataFrame:
    """Summarize finding volume and control diversity by resource."""
    return (
        findings_df
        .groupby("Resource")
        .agg(
            Findings=("ControlId", "size"),
            Controls=("ControlId", "nunique"),
        )
        .sort_values(
            ["Findings", "Controls"],
            ascending=False,
        )
    )
