"""
uv run tools/analyzer_status.py
"""

import boto3

SEPARATOR = "=" * 50
SUBSEPARATOR = "-" * 50


def print_analyzer(analyzer: dict) -> None:
    print(f"Name                : {analyzer.get('name', '-')}")
    print(f"Type                : {analyzer.get('type', '-')}")
    print(f"Status              : {analyzer.get('status', '-')}")
    print(f"ARN                 : {analyzer.get('arn', '-')}")


def main() -> None:
    client = boto3.client("accessanalyzer")

    response = client.list_analyzers()

    print("IAM Access Analyzer")
    print(SEPARATOR)
    print()

    analyzers = response.get("analyzers", [])

    print(f"Analyzers: {len(analyzers)}")
    print()

    for index, analyzer in enumerate(analyzers, start=1):
        print(f"Analyzer {index}")
        print(SUBSEPARATOR)
        print_analyzer(analyzer)
        print()


if __name__ == "__main__":
    main()
