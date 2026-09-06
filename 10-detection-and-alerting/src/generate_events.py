"""
Generate IAM policy-change events for the detection lab. 

uv run generate_events.py
"""

import json
import boto3

ROLE_NAME = "detection-lab-role"
POLICY_NAME = "detection-lab-policy"


BASELINE_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["s3:GetObject"],
            "Resource": "*",
        }
    ],
}

BROADER_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
            ],
            "Resource": "*",
        }
    ],
}


def put_policy(iam_client, policy: dict[str, object], description: str) -> None:
    """Replace the role's inline policy."""
    iam_client.put_role_policy(
        RoleName=ROLE_NAME,
        PolicyName=POLICY_NAME,
        PolicyDocument=json.dumps(policy),
    )
    print(description)


def main() -> None:
    iam_client = boto3.client("iam")

    put_policy(
        iam_client,
        BROADER_POLICY,
        "Applied broader policy.",
    )

    put_policy(
        iam_client,
        BASELINE_POLICY,
        "Restored baseline policy.",
    )


if __name__ == "__main__":
    main()
