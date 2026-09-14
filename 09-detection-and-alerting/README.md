# Detection and Alerting

## Problem

Security-relevant activity can occur even when individual AWS API requests are authorized. Repeated privileged changes, suspicious configuration activity, or unexpected administrative actions may indicate risk and require investigation.

Security teams need a way to detect suspicious events and route them for further analysis or response.

## Goal

Demonstrate how AWS CloudTrail events can be routed through Amazon EventBridge and matched against security detection rules using Terraform and Infrastructure as Code (IaC).

Use AWS Lambda to receive matched events and record the findings in CloudWatch Logs.

> **Note:** A CloudTrail trail must be configured separately for the CloudTrail → EventBridge detection path used in this lab.

## Architecture

```text
AWS API Activity
       │
       │
       ▼
CloudTrail
       │
       │ CloudTrail events
       ▼
EventBridge Default Bus
       │
       │ IAM event routing
       ▼
Detection Lab Event Bus
       │
       │ Detection rule
       │ PutRolePolicy
       ▼
AWS Lambda
       │
       │
       ▼
CloudWatch Logs
```

## Success Criteria

| Check                                            | Status |
| ------------------------------------------------ | :----: |
| Event pipeline and rule-based routing configured |   ✅   |
| Security events generated through code           |   ✅   |
| Target Lambda invoked and logs verified          |   ✅   |

## Key Observations

- IAM is a global AWS service. IAM API events are recorded in `us-east-1`, which became an important consideration when the initial lab deployment used `ap-south-1`.
- The regional mismatch provided a useful demonstration of how AWS global services can affect security monitoring architecture.
