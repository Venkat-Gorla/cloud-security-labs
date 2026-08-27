"""
Analyze AWS Security Hub findings with Pandas.

uv run tools/security_hub_analysis.py
"""

import json
from pathlib import Path
import pandas as pd
from df_output import (
    print_findings_summary,
    print_severity_summary,
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
    severity_order = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFORMATIONAL"]

    summary = findings_df["Severity"].value_counts()
    return summary.reindex(severity_order, fill_value=0)


def main() -> None:
    findings = load_findings(DATA_PATH)
    findings_df = create_findings_dataframe(findings)

    print_findings_summary(findings_df)

    severity_summary = summarize_findings_by_severity(findings_df)
    print_severity_summary(severity_summary)


if __name__ == "__main__":
    main()
