"""
uv run src/demo.py --role-arn <role-arn>
"""
from __future__ import annotations

import argparse
import boto3


def get_identity(client) -> dict:
    """Return the current AWS caller identity."""
    return client.get_caller_identity()


def assume_role(sts, role_arn: str) -> dict:
    """Assume an IAM role and return temporary credentials."""

    response = sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName="sts-lab-demo",
    )

    return response["Credentials"]


def create_assumed_session(credentials: dict) -> boto3.Session:
    """Create a new boto3 session using temporary credentials."""

    return boto3.Session(
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
    )


def list_buckets(assumed_session) -> list[str]:
    """Return the names of all S3 buckets visible to the assumed role."""
    s3 = assumed_session.client("s3")
    response = s3.list_buckets()

    return [bucket["Name"] for bucket in response["Buckets"]]


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--role-arn",
        required=True,
        help="IAM Role ARN to assume",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    sts = boto3.client("sts")

    print("=== Current Identity ===")
    identity = get_identity(sts)
    print(identity["Arn"])

    print("\nAssuming role...\n")
    credentials = assume_role(sts, args.role_arn)

    assumed_session = create_assumed_session(credentials)
    assumed_sts = assumed_session.client("sts")

    print("=== Assumed Identity ===")
    assumed_identity = get_identity(assumed_sts)
    print(assumed_identity["Arn"])

    print("\n=== Temporary Credentials ===")
    print(f"Access Key : {credentials['AccessKeyId']}")
    print(f"Expires    : {credentials['Expiration']}")

    print("\n=== S3 Buckets ===")
    for bucket in list_buckets(assumed_session):
        print(bucket)


if __name__ == "__main__":
    main()
