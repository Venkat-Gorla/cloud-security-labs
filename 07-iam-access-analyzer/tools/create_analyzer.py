"""
uv run tools/create_analyzer.py
"""

import boto3

SEPARATOR = "=" * 50


def create_analyzer(client, name: str) -> dict:
    return client.create_analyzer(
        analyzerName=name,
        type="ACCOUNT",
    )


def main() -> None:
    client = boto3.client("accessanalyzer")
    analyzer_name = "cloud-security-lab-07"

    response = create_analyzer(client, analyzer_name)

    print("IAM Access Analyzer")
    print(SEPARATOR)
    print()
    print(f"Name                : {response.get('arn', '-')}")
    print(f"Status              : {response.get('status', '-')}")
    print(f"Type                : ACCOUNT")
    print()


if __name__ == "__main__":
    main()
