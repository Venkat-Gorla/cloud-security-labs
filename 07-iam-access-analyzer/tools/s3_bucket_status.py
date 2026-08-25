"""
Inspect an S3 bucket configuration.

uv run tools/s3_bucket_status.py <bucket-name>
uv run tools/s3_bucket_status.py video-streaming-etag-demo-client
"""

import argparse
from pprint import pprint

import boto3
from botocore.exceptions import ClientError


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


def main() -> None:
    args = parse_args()

    client = boto3.client("s3")

    configurations = {
        "Bucket Location": get_configuration(
            get_bucket_location,
            client,
            args.bucket_name,
        ),
        "Website Configuration": get_configuration(
            get_bucket_website,
            client,
            args.bucket_name,
        ),
        "Public Access Block": get_configuration(
            get_public_access_block,
            client,
            args.bucket_name,
        ),
        "Bucket Policy": get_configuration(
            get_bucket_policy,
            client,
            args.bucket_name,
        ),
    }

    print("Amazon S3 Bucket Configuration")
    print("=" * 50)
    print()

    for name, response in configurations.items():
        print(name)
        print("-" * 50)
        pprint(response)
        print()


if __name__ == "__main__":
    main()
