"""
uv run tools/create_analyzer.py
"""

import boto3


def create_analyzer(client, name: str) -> dict:
    return client.create_analyzer(
        analyzerName=name,
        type="ACCOUNT",
    )


def main() -> None:
    client = boto3.client("accessanalyzer")
    response = create_analyzer(client, "cloud-security-lab-07")

    print("IAM Access Analyzer created")
    print()
    print(f"ARN : {response.get('arn', '-')}")


if __name__ == "__main__":
    main()
