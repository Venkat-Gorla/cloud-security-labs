"""
Analyze AWS Security Hub findings with Pandas.

uv run tools/security_hub_analysis.py
"""

import json
from pathlib import Path
import pandas as pd
from security_hub_prioritization import (
    find_high_priority_controls,
    summarize_findings_by_resource,
    summarize_finding_concentration,
)
from df_output import (
    print_findings_summary,
    print_severity_summary,
    print_control_summary,
    print_resource_type_summary,
    print_high_priority_controls,
    print_resource_summary,
    print_finding_concentration,
)

DATA_PATH = Path("data/security_hub_findings.json")


def save_findings(findings: list[dict], path: Path) -> None:
    """Save raw Security Hub findings to a local JSON snapshot."""
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(findings, file, indent=2, default=str)


def load_findings(path: Path) -> list[dict]:
    """Load Security Hub findings from a local JSON snapshot."""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def normalize_finding(finding: dict) -> dict:
    """Extract analytical fields from one Security Hub finding."""
    compliance = finding.get("Compliance", {})
    severity = finding.get("Severity", {})
    resources = finding.get("Resources", [])

    resource = resources[0] if resources else {}

    return {
        "ControlId": compliance.get("SecurityControlId", "-"),
        "ComplianceStatus": compliance.get("Status", "-"),
        "Severity": severity.get("Label", "-"),
        "ResourceType": resource.get("Type", "-"),
        "Resource": resource.get("Id", "-"),
        "WorkflowState": finding.get("WorkflowState", "-"),
        "RecordState": finding.get("RecordState", "-"),
        "Region": finding.get("Region", "-"),
        "Title": finding.get("Title", "-"),
        "CreatedAt": finding.get("CreatedAt", "-"),
        "UpdatedAt": finding.get("UpdatedAt", "-"),
    }


def create_findings_dataframe(findings: list[dict]) -> pd.DataFrame:
    """Create a normalized DataFrame from Security Hub findings."""
    normalized_findings = [
        normalize_finding(finding)
        for finding in findings
    ]

    return pd.DataFrame(normalized_findings)


def summarize_findings_by_severity(
    findings_df: pd.DataFrame,
) -> pd.Series:
    """Count findings by severity."""
    # vegorla: import from security_hub_prioritization
    severity_order = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFORMATIONAL"]

    summary = findings_df["Severity"].value_counts()
    return summary.reindex(severity_order, fill_value=0)


def summarize_findings_by_column(
    findings_df: pd.DataFrame,
    column: str,
) -> pd.Series:
    """Count findings grouped by a DataFrame column."""
    return findings_df[column].value_counts()


# vegorla: check if this function is needed, it seems to be unused
def summarize_findings_by_resource_and_control(
    findings_df: pd.DataFrame,
) -> pd.DataFrame:
    """Count findings by resource type and security control."""
    summary = (
        findings_df
        .groupby(["ResourceType", "ControlId"])
        .size()
        .reset_index(name="Findings")
        .sort_values(
            ["ResourceType", "Findings"],
            ascending=[True, False],
        )
    )

    return summary


def summarize_findings_by_control_and_severity(
    findings_df: pd.DataFrame,
) -> pd.DataFrame:
    """Count findings by security control and severity."""
    severity_order = [
        "CRITICAL",
        "HIGH",
        "MEDIUM",
        "LOW",
        "INFORMATIONAL",
    ]

    summary = (
        findings_df
        .groupby(["ControlId", "Severity"])
        .size()
        .unstack(fill_value=0)
    )

    return summary.reindex(columns=severity_order, fill_value=0)


def main() -> None:
    findings = load_findings(DATA_PATH)
    findings_df = create_findings_dataframe(findings)

    print_findings_summary(findings_df)

    severity_summary = summarize_findings_by_severity(findings_df)
    print_severity_summary(severity_summary)
    print()

    control_summary = summarize_findings_by_column(findings_df, "ControlId",)
    print_control_summary(control_summary)
    print()

    resource_type_summary = summarize_findings_by_column(
        findings_df,
        "ResourceType",
    )
    print_resource_type_summary(resource_type_summary)
    print()

    high_priority_controls = find_high_priority_controls(findings_df)
    print_high_priority_controls(high_priority_controls)
    print()

    resource_summary = summarize_findings_by_resource(findings_df)
    print_resource_summary(resource_summary, limit=15)
    print()

    concentration = summarize_finding_concentration(
        resource_summary,
        [1, 5, 10, 20],
    )
    print_finding_concentration(concentration, len(findings_df),)


if __name__ == "__main__":
    main()
