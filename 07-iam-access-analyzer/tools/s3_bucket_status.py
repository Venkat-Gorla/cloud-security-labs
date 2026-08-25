"""
Inspect an S3 bucket configuration.

uv run tools/s3_bucket_status.py <bucket-name>
uv run tools/s3_bucket_status.py video-streaming-etag-demo-client
"""

import argparse
import json

import boto3
from botocore.exceptions import ClientError

from output import print_bucket_configuration


def get_bucket_location(client, bucket_name: str) -> dict:
    return client.get_bucket_location(Bucket=bucket_name)


def get_bucket_website(client, bucket_name: str) -> dict:
    return client.get_bucket_website(Bucket=bucket_name)


def get_public_access_block(client, bucket_name: str) -> dict:
    return client.get_public_access_block(Bucket=bucket_name)


def get_bucket_policy(client, bucket_name: str) -> dict:
    return client.get_bucket_policy(Bucket=bucket_name)


def get_configuration(
    function,
    client,
    bucket_name: str,
) -> dict:
    try:
        return function(client, bucket_name)
    except ClientError as error:
        error_code = error.response.get("Error", {}).get("Code", "")

        if error_code in {
            "NoSuchWebsiteConfiguration",
            "NoSuchPublicAccessBlockConfiguration",
            "NoSuchBucketPolicy",
        }:
            return {}

        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect an S3 bucket configuration."
    )
    parser.add_argument("bucket_name")
    return parser.parse_args()


def parse_policy(response: dict) -> list[dict]:
    policy = response.get("Policy")

    if not policy:
        return []

    document = json.loads(policy)
    statements = document.get("Statement", [])

    if isinstance(statements, dict):
        return [statements]

    return statements


def get_region(location: dict) -> str:
    return location.get("LocationConstraint") or "us-east-1"


def main() -> None:
    args = parse_args()
    client = boto3.client("s3")

    location = get_configuration(
        get_bucket_location,
        client,
        args.bucket_name,
    )
    website = get_configuration(
        get_bucket_website,
        client,
        args.bucket_name,
    )
    public_access_block = get_configuration(
        get_public_access_block,
        client,
        args.bucket_name,
    )
    policy = get_configuration(
        get_bucket_policy,
        client,
        args.bucket_name,
    )

    print_bucket_configuration(
        bucket_name=args.bucket_name,
        region=get_region(location),
        website=website,
        public_access_block=public_access_block,
        policy_statements=parse_policy(policy),
    )


if __name__ == "__main__":
    main()
