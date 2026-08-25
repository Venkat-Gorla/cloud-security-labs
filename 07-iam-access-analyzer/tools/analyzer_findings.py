"""
Inspect IAM Access Analyzer findings.

uv run tools/analyzer_findings.py
"""

import boto3
from output import print_finding

ANALYZER_NAME = "cloud-security-lab-07"
SEPARATOR = "=" * 50


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
    print(f"Findings: {len(findings)}\n")

    for number, finding in enumerate(findings, start=1):
        print_finding(finding, number)


if __name__ == "__main__":
    main()
