"""
Inspect IAM Access Analyzer findings.

uv run tools/analyzer_findings.py
"""

from pprint import pprint
import boto3


ANALYZER_NAME = "cloud-security-lab-07"


def get_analyzer(client, name: str) -> dict | None:
    response = client.list_analyzers()

    for analyzer in response.get("analyzers", []):
        if analyzer.get("name") == name:
            return analyzer

    return None


def get_findings(client, analyzer_arn: str) -> dict:
    return client.list_findings(
        analyzerArn=analyzer_arn,
    )


def main() -> None:
    client = boto3.client("accessanalyzer")
    analyzer = get_analyzer(client, ANALYZER_NAME)

    if analyzer is None:
        raise RuntimeError(
            f"IAM Access Analyzer not found: {ANALYZER_NAME}"
        )

    response = get_findings(client, analyzer["arn"])

    print("IAM Access Analyzer Findings")
    print("=" * 50)
    print()
    print("Raw API Response")
    print("-" * 50)
    pprint(response)


if __name__ == "__main__":
    main()
