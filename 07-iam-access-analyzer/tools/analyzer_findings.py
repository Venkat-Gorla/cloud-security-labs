"""
Inspect IAM Access Analyzer findings.

uv run tools/analyzer_findings.py
"""

import boto3


ANALYZER_NAME = "cloud-security-lab-07"

SEPARATOR = "=" * 50
SUBSEPARATOR = "-" * 50


def get_analyzer(client, name: str) -> dict | None:
    response = client.list_analyzers()

    for analyzer in response.get("analyzers", []):
        if analyzer.get("name") == name:
            return analyzer

    return None


def get_findings(client, analyzer_arn: str) -> list[dict]:
    response = client.list_findings(
        analyzerArn=analyzer_arn,
    )
    return response.get("findings", [])


def format_principals(principal: dict) -> str:
    values = []

    for principal_type, principal_value in principal.items():
        values.append(f"{principal_type}: {principal_value}")

    return ", ".join(values) if values else "-"


def print_finding(finding: dict, number: int) -> None:
    actions = finding.get("action", [])
    action_text = ", ".join(actions) if actions else "-"

    print(f"Finding {number}")
    print(SUBSEPARATOR)
    print(f"Resource Type       : {finding.get('resourceType', '-')}")
    print(f"Resource            : {finding.get('resource', '-')}")
    print(
        f"Principal           : {format_principals(finding.get('principal', {}))}")
    print(f"Action              : {action_text}")
    print(f"Public              : {finding.get('isPublic', '-')}")
    print(f"Status              : {finding.get('status', '-')}")
    print(
        f"Source              : {', '.join(source.get('type', '-') for source in finding.get('sources', []))}")
    print(f"Analyzed At         : {finding.get('analyzedAt', '-')}")
    print()


def main() -> None:
    client = boto3.client("accessanalyzer")
    analyzer = get_analyzer(client, ANALYZER_NAME)

    if analyzer is None:
        raise RuntimeError(
            f"IAM Access Analyzer not found: {ANALYZER_NAME}"
        )

    findings = get_findings(client, analyzer["arn"])

    print("IAM Access Analyzer Findings")
    print(SEPARATOR)
    print()
    print(f"Findings: {len(findings)}")
    print()

    for number, finding in enumerate(findings, start=1):
        print_finding(finding, number)


if __name__ == "__main__":
    main()
