# Lab 01 - CloudTrail Forensics

## Problem

CloudTrail contains a complete audit history of AWS management activity, but identifying meaningful human actions from thousands of events can be time-consuming.

## Goal

Build a lightweight Python tool to analyze CloudTrail management events and summarize IAM user activity by service, API operation, and request origin.

## Success Criteria

| Check                                              | Status |
| -------------------------------------------------- | :----: |
| CloudTrail IAM user activity analyzed              |   ✅   |
| Activity summarized by service, action, and origin |   ✅   |
| Forensic activity report generated                 |   ✅   |

## Practical Security Uses

- Investigate unexpected AWS changes.
- Review IAM user activity over a configurable time period.
- Distinguish Console activity from SDK or CLI automation.
- Understand which AWS services are actively being used.
- Build a foundation for custom security analytics and forensic tooling.

## Limitations

- Analyzes CloudTrail **management events** only.
- Does not analyze CloudTrail **data events** (for example, S3 object access or DynamoDB item operations).
- Supports analysis for a single IAM user per execution.
